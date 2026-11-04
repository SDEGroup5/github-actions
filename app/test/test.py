"""
This module contain the test for the PostgreConnector class
"""

import json
import threading
from functools import partial
from http.client import HTTPConnection, HTTPResponse
from http.server import HTTPServer

import pytest  # pylint: disable=import-error
from src.controller.json_controller import JsonController
from src.router.abstraction.i_router import IRouter
from src.router.json_router import JsonRouter
from src.server.server import Server

# Server tests
# pylint: disable=duplicate-code
# Lines are duplicate with main since integration testing follows common code

def test_server_get_successful():
    '''
    Test if the server component is able to answer correctly to a
    GET request
    '''

    json_path: str = "./app/json/data.json"
    json_data: str = ""

    try:
        with open(json_path, encoding="utf-8") as file:
            data = json.load(file)
            json_data = json.dumps(data)
    except (FileNotFoundError, json.JSONDecodeError):
        pytest.fail("JSON file not found")

    json_controller: JsonController = JsonController(json_path)

    json_router: IRouter = JsonRouter(json_controller)

    router_dict: dict[str, IRouter] = {"json": json_router}

    server_partial: partial[Server] = partial(Server,
                                              endpoint_routers=router_dict)

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
    con.request("GET", "/json/getData", headers=header)

    response: HTTPResponse = con.getresponse()

    con.close()

    # Shutdown server and end the thread
    server.shutdown()
    server.server_close()
    server_thread.join()

    assert json.loads(response.read().decode("utf-8")) == {"data": json_data}
    assert response.status == 200


@pytest.mark.parametrize(
    "endpoint, json_path, expected_status, expected_response",
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

    json_controller: JsonController = JsonController(path)

    json_router: IRouter = JsonRouter(json_controller)

    router_dict: dict[str, IRouter] = {"json": json_router}

    server_partial: partial[Server] = partial(Server,
                                              endpoint_routers=router_dict)

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
    con.request("GET", endpoint, headers=header)

    response: HTTPResponse = con.getresponse()

    con.close()

    # Shutdown server and end the thread
    server.shutdown()
    server.server_close()
    server_thread.join()

    assert json.loads(response.read().decode("utf-8")) == expected_response
    assert response.status == expected_st
