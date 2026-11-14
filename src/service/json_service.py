"""
This module contains JsonService: it is responsible for managing
the JSON file
"""

import json


class JsonService:  # pylint: disable=too-few-public-methods
    """
    JsonService: perform actions on the JSON file
    """

    json_file_path: str

    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def read_json_file(self) -> str | None:
        """
        Read the JSON file and return its content
        """

        try:
            with open(self.json_file_path, encoding="utf-8") as file:
                data = json.load(file)
                return json.dumps(data)

        except (FileNotFoundError, json.JSONDecodeError):
            return None
