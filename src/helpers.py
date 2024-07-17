import math
from src.config import *
from os import listdir, path


def import_assets(asset_path):
    frames = []
    for image_path in listdir(asset_path):
        if image_path.endswith(".png"):
            frames.append(pygame.image.load(path.join(asset_path, image_path)).convert_alpha())
    return frames


def import_image(image_path):
    return pygame.image.load(image_path).convert_alpha()


def generate_circular_waypoints(width, height):
    center_x, center_y = width / 2, height / 2
    radius = 50
    num_points = 150

    # waypoints = []
    waypoints = [(width + 30, center_y), (center_x, center_y)]
    for i in range(num_points):
        angle = i * (2 * math.pi / num_points)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        waypoints.append((x, y))
    waypoints.append((-30, center_y))
    return waypoints

