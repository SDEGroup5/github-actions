"""Main file"""

from functools import partial
from http.server import HTTPServer

from dotenv import dotenv_values  # pylint: disable=import-error
from src.controller.abstraction.i_controller import IController
from src.controller.json_controller import JsonController
from src.server.server import Server
from src.service.json_service import JsonService


def main():
    """
    Main function
    """

    config = dotenv_values("/run/secrets/my_secret")
    json_path: str = str(config.get("DATA_PATH", "./json/data.json"))

    json_service: JsonService = JsonService(json_path)

    json_controller: IController = JsonController(json_service)

    controller_dict: dict[str, IController] = {"json": json_controller}

    server_partial: partial[Server] = partial(
        Server, endpoint_controllers=controller_dict)

    server = HTTPServer(("0.0.0.0", 5000), server_partial)

    print("Server has started!")

    server.serve_forever()


if __name__ == "__main__":
    main()
