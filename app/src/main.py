"""Main file"""

from functools import partial
from http.server import HTTPServer

from dotenv import dotenv_values  # pylint: disable=import-error
from src.controller.json_controller import JsonController
from src.router.abstraction.i_router import IRouter
from src.router.json_router import JsonRouter
from src.server.server import Server


def main():
    """
    Main function
    """

    config = dotenv_values("/run/secrets/my_secret")
    json_path: str = str(config.get("DATA_PATH", "./json/data.json"))

    json_controller: JsonController = JsonController(json_path)

    json_router: IRouter = JsonRouter(json_controller)

    router_dict: dict[str, IRouter] = {"json": json_router}

    server_partial: partial[Server] = partial(Server,
                                              endpoint_routers=router_dict)

    server = HTTPServer(("0.0.0.0", 5000), server_partial)

    print("Server has started!")

    server.serve_forever()


if __name__ == "__main__":
    main()
