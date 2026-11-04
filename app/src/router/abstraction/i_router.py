"""
Contains the IRouter Interface. Each router should
implement it
"""

from abc import ABC, abstractmethod


class IRouter(ABC):  # pylint: disable=too-few-public-methods
    '''
    IRouter interface: routers are responsible of handling endpoints
    of a specific route
    '''

    @abstractmethod
    def handle_request(self, endpoint: str) -> tuple[bool, bytes]:
        '''
        Call the function that routes the specified request to the
        appropriate controller and controller method.

        Returns true and the encoded response if an handler for the
        specified endpoint was found, false otherwise
        '''
