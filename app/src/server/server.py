"""
This module contains the Server class which collect the user request
and pass them to the appropriate router
"""

import json
from http.server import BaseHTTPRequestHandler
from socket import socket
from socketserver import BaseServer
from typing import Any

from src.router.abstraction.i_router import IRouter


class Server(BaseHTTPRequestHandler):
    """
    This class provides the endpoints that route the requests to
    the appropriate routers
    """

    endpoint_routers: dict[str, IRouter]

    def __init__(self, request: socket, client_address: Any,
                 server: BaseServer, endpoint_routers: dict[str, IRouter]):
        # Register routers for specific routes
        self.endpoint_routers = endpoint_routers

        # Initialize the base class
        super().__init__(request, client_address, server)

    def do_GET(self):  # pylint: disable=invalid-name
        """
        Manages the GET requests. Only one endpoint is available: 
        /json, to get the current data included in the JSON file
        """
        base_endpoint: str = self.path.strip("/").split("/", 1)[0]

        router: IRouter | None = self.endpoint_routers.get(base_endpoint)

        if router is None:
            self.send_json({"error": "Endpoint not found"}, 404)
            return

        specific_endpoint = self.path.strip("/").removeprefix(
            base_endpoint).strip("/")

        result: tuple[bool, bytes] = router.handle_request(specific_endpoint)

        if result[0] is False:
            # See IRouter for documentation
            self.send_json({"error": "Endpoint not found"}, 404)
            return

        if len(result[1]) == 0:
            self.send_json({"error": "Internal server error"}, 500)
            return

        self.send_json({"data": result[1].decode()}, 200)

    def send_json(self, data: dict, status: int):
        '''
        Helper function: send a JSON structured answer
        '''

        response: bytes = json.dumps(data).encode("utf-8")
        header: dict = {
            "Content-Type": "application/json",
            "Content-Length": str(len(response)),
            "Access-Control-Allow-Origin": "*"
        }

        self.send_response(status)

        for key, v in header.items():
            self.send_header(key, v)

        self.end_headers()
        self.wfile.write(response)
