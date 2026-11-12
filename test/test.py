"""
This module contains the tests for the application
"""

import json
import threading
from functools import partial
from http.client import HTTPConnection, HTTPResponse
from http.server import HTTPServer

import pytest  # pylint: disable=import-error

from src.controller.abstraction.i_controller import IController
from src.controller.json_controller import JsonController
from src.server.server import Server
from src.service.json_service import JsonService

# Server tests
# pylint: disable=duplicate-code
# Lines are duplicate with main since integration testing follows common code


def create_and_contact_server(method: str, url: str,
                              json_path: str) -> tuple[bytes, int]:
    '''
    Resuable function: call the application server with the given method
    at the given url. json_path is needed to build the necessary
    components used by the server.

    Returns the bytes and the code of the server response.
    '''

    json_service: JsonService = JsonService(json_path)

    json_controller: IController = JsonController(json_service)

    controller_dict: dict[str, IController] = {"json": json_controller}
    server_partial: partial[Server] = partial(
        Server, endpoint_controllers=controller_dict)

    server = HTTPServer(("0.0.0.0", 5000), server_partial)

    # Run the server in another thread to avoid blocking the current test
    server_thread: threading.Thread = threading.Thread(
        target=server.serve_forever)

    # Start the thread with the server
    server_thread.start()

    # Prepare the header
    header: dict = {
        "Content-Type": "application/json",
    }

    con: HTTPConnection = HTTPConnection("127.0.0.1", 5000)
    con.request(method=method, url=url, headers=header)

    response: HTTPResponse = con.getresponse()

    response_bytes: bytes = response.read()
    response_code: int = response.status

    con.close()

    # Shutdown server and end the thread
    server.shutdown()
    server.server_close()
    server_thread.join()

    return response_bytes, response_code


def test_server_get_successful():
    '''
    Test if the server component is able to answer correctly to a
    GET request
    '''

    json_path: str = "./json/data.json"
    json_data: str = ""

    try:
        with open(json_path, encoding="utf-8") as file:
            data = json.load(file)
            json_data = json.dumps(data)
    except (FileNotFoundError, json.JSONDecodeError):
        pytest.fail("JSON file not found")

    response: tuple[bytes,
                    int] = create_and_contact_server("GET", "/json/getData",
                                                     json_path)

    assert json.loads(response[0].decode("utf-8")) == {"data": json_data}
    assert response[1] == 200


@pytest.mark.parametrize(
    "endpoint, path, expected_st, expected_response",
    [("/number", "/json/data.json", 404, {
        "error": "Endpoint not found"
    }),
     ("/json/getData", "/non/existent/dir/data.json", 500, {
         "error": "Internal server error"
     })],
)
def test_server_get_failure(endpoint: str, path: str, expected_st: int,
                            expected_response: dict):
    '''
    Test various kind of failures during a GET request to the Server
    component
    '''

    response: tuple[bytes,
                    int] = create_and_contact_server("GET", endpoint, path)

    assert json.loads(response[0].decode("utf-8")) == expected_response
    assert response[1] == expected_st
