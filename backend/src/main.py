"""Main file"""

from functools import partial
from http.server import HTTPServer

from dotenv import dotenv_values  # pylint: disable=import-error
from src.abstraction.i_postgre_connector import IPostgreConnector
from src.abstraction.i_server_handler import IServerHandler
from src.postgre_connector import PostgreConnector
from src.server import Server
from src.server_handler import ServerHandler


def main():
    """Main function for testing purposes."""

    config = dotenv_values("/run/secrets/my_secret")

    username: str = str(config.get("POSTGRES_USER", "myuser"))
    psw: str = str(config.get("POSTGRES_PASSWORD", "secret_password"))
    db_name: str = str(config.get("POSTGRES_DB", "TheDatabase"))

    connector: IPostgreConnector = PostgreConnector("database", "5432",
                                                    db_name, username, psw)

    server_handler: IServerHandler = ServerHandler(connector)

    server_partial: partial[Server] = partial(Server,
                                              server_handler=server_handler)

    server = HTTPServer(("0.0.0.0", 5000), server_partial)

    server.serve_forever()


if __name__ == "__main__":
    main()
