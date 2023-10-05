import json


def load_level_data():
    """Return level data"""
    with open("data/levels.json", "r") as json_file:
        level_data = json.load(json_file)
    return level_data["levels_constants"]


def get_level_info(level, levels_data):
    """Return level info"""
    if levels_data and f"level{level}" in levels_data:
        return levels_data[f"level{level}"]
