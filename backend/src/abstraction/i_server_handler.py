"""
Contains IServerHandler interface, links requests with IPostgreConnector
"""

from abc import ABC, abstractmethod


class IServerHandler(ABC):
    '''
    IServer interface, links requests with IPostgreConnector
    '''

    @abstractmethod
    def write_number_request_handler(self, number: int) -> int | None:
        '''
        Ask the Postgre connector to write the number.

        If the process succeed, the same number is returned, otherwise None is returned instead
        '''

    @abstractmethod
    def read_number_request_handler(self) -> int | None:
        '''
        Ask the Postgre connector to read the current number.
        
        If the process succeed, the number is returned, otherwise None is returned instead
        '''
