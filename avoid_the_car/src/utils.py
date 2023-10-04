import json


def load_level_data():
    """Return level data"""
    with open("data/levels.json", "r") as json_file:
        level_data = json.load(json_file)
    return level_data["levels_constants"]
