"""
Contains the IController Interface. Each controller should
implement it
"""

from abc import ABC, abstractmethod


class IController(ABC):  # pylint: disable=too-few-public-methods
    '''
    IController interface: controllerss are responsible of handling endpoints
    of a specific route
    '''

    @abstractmethod
    def handle_request(self, endpoint: str) -> tuple[bool, bytes]:
        '''
        Call the function that routes the specified request to the
        appropriate service and service method.

        Returns true and the encoded response if an handler for the
        specified endpoint was found, false otherwise
        '''
