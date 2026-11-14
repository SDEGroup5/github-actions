"""
This module contains json_controller: it is responsible of routing /json endpoints
"""

from collections.abc import Callable

from src.controller.abstraction.i_controller import IController
from src.service.json_service import JsonService


class JsonController(IController):
    """
    JsonController: route /json endpoints
    """

    endpoints_callable_dict: dict[str, Callable[[], bytes]]
    json_service: JsonService

    def __init__(self, json_service: JsonService):
        # Register routes with respective handler
        self.endpoints_callable_dict = {"getData": self.get_data}
        self.json_service = json_service

    def handle_request(self, endpoint: str) -> tuple[bool, bytes]:
        '''
        Call the function that routes the specified request to the
        appropriate service and service method.

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
        data: str | None = self.json_service.read_json_file()

        if data is None:
            return b""

        return data.encode("utf-8")
