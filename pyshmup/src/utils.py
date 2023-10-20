import json


class Config:
    def __init__(self):

        with open("data/config.json", "r") as json_file:
            self.data = json.load(json_file)

    def color(self):
        return self.data["colors"]
