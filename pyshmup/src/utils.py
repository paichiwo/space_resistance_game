import json


class Config:
    """Returns values from data/config.json"""
    def __init__(self):

        with open("data/config.json", "r") as json_file:
            self.data = json.load(json_file)

    def color(self):
        return self.data["colors"]

    def enemy_choices(self):
        return self.data["enemy_choices"]
