"""
Contains IPostgreConnector interface, allowing connection and operation to the postgresql
"""

from abc import ABC, abstractmethod

import psycopg2  # pylint: disable=import-error


class IPostgreConnector(ABC):
    '''
    IPostgreConnector interface, which allow connection and operation to the postgresql database
    '''

    @abstractmethod
    def open_connection(self) -> psycopg2.extensions.connection | None:
        '''
        Implement connection method.

        Should return the connection if successful, otherwise None.
        '''

    @abstractmethod
    def write_number(self, number: int) -> int | None:
        '''Write the specified number to the database.

        Should return the number itself if it was written, otherwise None.
        '''

    @abstractmethod
    def get_number(self) -> int | None:
        '''Return the number from the database, or None if unsuccessful.'''

    @abstractmethod
    def close_connection(self, conn: psycopg2.extensions.connection) -> bool:
        '''Return True if the connection was successfully closed, otherwise False.'''

    @abstractmethod
    def create_db(self, db_name: str) -> bool:
        '''Return True if the database and table are initialized successfully'''
