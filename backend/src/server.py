"""
This module contains the Server class which provides the application endpoints
"""

import json
from http.server import BaseHTTPRequestHandler
from socket import socket
from socketserver import BaseServer
from typing import Any

from src.abstraction.i_server_handler import IServerHandler


class Server(BaseHTTPRequestHandler):
    """
    This class provides the endpoints that manages requests to the
    application logic (ServerHandler), which communicate with the 
    Postgre connector
    """

    server_handler: IServerHandler

    def __init__(self, request: socket, client_address: Any,
                 server: BaseServer, server_handler: IServerHandler):
        self.server_handler = server_handler
        super().__init__(request, client_address, server)

    def do_GET(self):  # pylint: disable=invalid-name
        '''
        Manage the GET requests. Only one endpoint is available: 
        /number, to get the current value

        If successful, the response will contain a payload like
        {"number": 3} (with the current number), otherwise an
        error message like {"error": "Internal error"}

        pylint ignored since it must retain the name
        '''
        if self.path == "/number":
            result: int | None = self.server_handler.read_number_request_handler(
            )
            if result is not None:
                self.send_json({"number": result}, 200)
            else:
                self.send_json({"error": "Internal error"}, 500)
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_PUT(self):  # pylint: disable=invalid-name
        '''
        Manage the PUT requests. Only one endpoint is available:
        /number, that updates the current value

        Needs the PUT request to have Content-Length set and a JSON
        formatted payload like {"number":3}

        The response will contain {"success": result} where result
        is the value returned by the IServerHandler when successful,
        or {"error": "Internal error"} or similar structure in case
        of unsuccessful response

        pylint ignored since it must retain the name
        '''
        if self.path == "/number":
            try:
                content_length: int = int(self.headers.get(
                    "Content-Length", 0))

                if content_length == 0:
                    self.send_json({"error": "Bad request"}, 400)
                    return

                body: bytes = self.rfile.read(content_length)
                data: Any = json.loads(body)

                if not isinstance(data, dict):
                    self.send_json({"error": "Bad request"}, 400)
                    return

                value = data.get("number")

                if not isinstance(value, int):
                    self.send_json({"error": "Bad request"}, 400)
                    return

                # Safe conversion, value has been checked and it is an int
                result: int | None = self.server_handler.write_number_request_handler(
                    int(value))

                if result is not None:
                    self.send_json({"success": result}, 200)
                else:
                    self.send_json({"error": "Internal error"}, 500)
            except (ValueError, json.JSONDecodeError):
                self.send_json({"error": "Bad request"}, 400)
        else:
            self.send_json({"error": "Not found"}, 404)

    def send_json(self, data: dict, status: int):
        '''
        Helper function: send a JSON structured answer
        '''
        response: bytes = json.dumps(data).encode("utf-8")
        header: dict = {
            "Content-Type": "application/json",
            "Content-Length": str(len(response))
        }

        self.send_response(status)

        for key, v in header.items():
            self.send_header(key, v)

        self.end_headers()
        self.wfile.write(response)
