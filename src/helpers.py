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
    radius = 100
    num_points = 150

    waypoints = [(width + 30, start_y)]
    for i in range(num_points):
        angle = i * (2 * math.pi / num_points)
        x = start_x + radius * math.cos(angle)
        y = start_y + radius * math.sin(angle)
        waypoints.append((x, y))
    waypoints.append((-51, start_y-5))
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


def curve_waypoints(width, height):
    waypoints = []
    num_points = 100  # Total number of points for the smooth curve
    start_x, start_y = -50, height / 2  # Start off-screen on the left
    end_x, end_y = width + 50, height / 4  # End off-screen on the right, with a rise

    waypoints.append((start_x, start_y))

    for i in range(1, num_points + 1):
        t = i / num_points
        # Quadratic Bezier curve control points
        control_x, control_y = width / 3, height

        # Quadratic Bezier formula
        x = (1 - t) ** 2 * start_x + 2 * (1 - t) * t * control_x + t ** 2 * end_x
        y = (1 - t) ** 2 * start_y + 2 * (1 - t) * t * control_y + t ** 2 * end_y

        waypoints.append((x, y))

    return waypoints


def down_left_right_waypoints(width, height):
    waypoints = []
    num_points = 200  # Total number of points for the enemy movement path
    move_down_distance = 50  # Distance the enemy moves down before starting horizontal movement
    oscillation_amplitude = 100  # Amplitude of the left-right oscillation
    oscillation_frequency = 2  # Number of oscillations over the total path

    for i in range(num_points):
        t = i / (num_points - 1)
        print(t)

        if t < 0.5:  # Move down phase
            y = height * t  # Moves down from the top of the screen to `move_down_distance`
            x = width / 2  # Set x position in the center (or adjust based on your need)
        else:  # Oscillate phase
            t = (t * 2)  # Normalize t to range [0, 1] for oscillation
            x = width / 2 + oscillation_amplitude * math.sin(oscillation_frequency * t * 2 * math.pi)
            y = height * 0.5 + move_down_distance  # Maintain the y position from the end of the down phase

        waypoints.append((x, y))

    return waypoints
