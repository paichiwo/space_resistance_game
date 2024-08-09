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


def circular_waypoints(width, height):
    start_x, start_y = width / 2, height / 2 - 30
    radius = 50
    num_points = 150

    waypoints = [(width + 30, start_y)]
    for i in range(num_points):
        angle = i * (2 * math.pi / num_points)
        x = start_x + radius * math.cos(angle)
        y = start_y + radius * math.sin(angle)
        waypoints.append((x, y))
    waypoints.append((-50, start_y - 3))
    return waypoints


def sine_wave_waypoints(width, height):
    waypoints = []

    start_x, start_y = 50, 0
    end_x, end_y = width, 0
    amplitude = 200
    wavelength = math.pi / 2
    num_points = 150

    for i in range(num_points):
        t = i / (num_points - 1)
        x = start_x + t * (end_x - start_x)
        y = start_y + amplitude * math.sin(2 * math.pi * t / wavelength)
        waypoints.append((x, y))
    return waypoints
