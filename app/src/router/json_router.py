"""
This module contains json_router: it is responsible of routing /json endpoints
"""

from collections.abc import Callable

from src.controller.json_controller import JsonController
from src.router.abstraction.i_router import IRouter


class JsonRouter(IRouter):
    """
    JsonRouter: route /json endpoints
    """

    endpoints_callable_dict: dict[str, Callable[[], bytes]]
    json_controller: JsonController

    def __init__(self, json_controller: JsonController):
        # Register routing with respective handler
        self.endpoints_callable_dict = {"getData": self.get_data}
        self.json_controller = json_controller

    def handle_request(self, endpoint: str) -> tuple[bool, bytes]:
        '''
        Call the function that routes the specified request to the
        appropriate controller and controller method.

        Returns true and the encoded response if an handler for the specified endpoint was found,
        false otherwise
        '''

        # Try to search the handler for the specified endpoint
        handler: Callable | None = self.endpoints_callable_dict.get(endpoint)

        if handler is None:
            # No handler was found
            return False, b""

        return True, handler()

    def get_data(self) -> bytes:
        '''
        Handles /json/getData: should return the bytes representing
        the encoded answer
        '''
        data: str | None = self.json_controller.read_json_file()

        if data is None:
            return b""

        return data.encode("utf-8")
