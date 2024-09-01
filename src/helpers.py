import math
from src.config import *
from os import listdir, path


def import_assets(asset_path):
    frames = []
    for image_path in listdir(asset_path):
        if image_path.endswith('.png'):
            frames.append(pygame.image.load(path.join(asset_path, image_path)).convert_alpha())
    return frames


def import_image(image_path):
    return pygame.image.load(image_path).convert_alpha()


def circular_path(width, height, direction='left'):
    start_x, start_y = width / 2, height / 2 - 30
    end_x, end_y = (-50, start_y - 2) if direction == 'right' else (width + 50, start_y + 2)
    radius = 50
    num_points = 150

    waypoints, angle_direction = ([(width, start_y)], 1) if direction == 'right' else ([(-30, start_y)], -1)
    for i in range(num_points):
        angle = i * (2 * math.pi / num_points) * angle_direction
        x = start_x + radius * math.cos(angle)
        y = start_y + radius * math.sin(angle)
        waypoints.append((x, y))

    waypoints.append((end_x, end_y))
    return waypoints


def s_shape_path(width, height, direction='left', start_y=100):
    amplitude = 30  # Controls the vertical "height" of the S-shape curve
    wavelength = width / 4  # Controls the horizontal length of each wave in the S-shape
    num_points = 200  # Number of waypoints to generate

    # Determine start and end points based on the direction
    start_x = -20 if direction == 'left' else width + 20
    end_x = width + 50 if direction == 'left' else -50

    # Determine the direction of the x increment
    x_increment = (end_x - start_x) / num_points

    # Generate the S-shaped path
    waypoints = []
    for i in range(num_points):
        t = i / num_points
        x = start_x + i * x_increment
        y = start_y + amplitude * math.sin(2 * math.pi * t * 2)  # The factor of 2 creates the "S" shape
        waypoints.append((x, y))

    return waypoints


def sine_wave_path(width, height, direction='left'):
    amplitude = height - 90  # Wave height
    wavelength = math.pi / 2
    num_points = 150

    start_x, end_x = (38, width) if direction == 'left' else (width - 38, 0)

    waypoints = []
    for i in range(num_points):
        t = i / (num_points - 1)
        x = start_x + t * (end_x - start_x)
        y = amplitude * math.sin(2 * math.pi * t / wavelength)
        waypoints.append((x, y))
    return waypoints


def diagonal_path(width, height, direction='left'):
    start_x = -20 if direction == 'right' else width + 20
    start_y = -20
    waypoint_increment = 20

    waypoints = []
    x, y = start_x, start_y
    while y <= height:
        waypoints.append((x, y))
        x += waypoint_increment if direction == 'right' else -waypoint_increment
        y += waypoint_increment

    waypoints.append((266, 240) if direction == 'right' else (-50, 240))
    return waypoints


def down_and_oscillate_path(width, height, y_pos=160):
    # Phase 1: Move down
    start_x, start_y = width / 2, -20
    vertical_waypoints = []

    current_y = start_y
    while current_y < y_pos:
        vertical_waypoints.append((start_x, current_y))
        current_y += 5

    # Phase 2: Oscillate left and right at y_pos
    oscillation_amplitude = width / 2 - 115  # Distance from center to the edge
    num_points_per_oscillation = 50
    repeats = 5
    oscillation_waypoints = []

    for i in range(repeats):
        for direction in [1, -1]:  # Right then Left
            for j in range(num_points_per_oscillation):
                t = j / num_points_per_oscillation
                x = start_x + direction * oscillation_amplitude * t
                oscillation_waypoints.append((x, y_pos))
        oscillation_waypoints.append((start_x, y_pos))

    waypoints = vertical_waypoints + oscillation_waypoints
    return waypoints


def diagonal_and_oscillate_path(width, height, direction='left'):
    # Phase 1: Diagonal Movement
    start_x = -20 if direction == 'right' else width + 20
    start_y = -20
    end_y = height / 4  # 1/4 of the screen height
    diagonal_waypoints = []

    # Calculate diagonal path
    x, y = start_x, start_y
    while y < end_y:
        diagonal_waypoints.append((x, y))
        x += 5 if direction == 'right' else -5
        y += 5

    # Phase 2: Oscillate Up and Down along the diagonal path
    oscillation_amplitude = 10  # Oscillation amplitude in pixels
    num_oscillations = 5
    oscillation_waypoints = []

    for i in range(num_oscillations):
        # Move back along the diagonal
        for _ in range(oscillation_amplitude):
            x -= 1 if direction == 'right' else -1
            y -= 1
            oscillation_waypoints.append((x, y))
        # Move forward along the diagonal
        for _ in range(oscillation_amplitude):
            x += 1 if direction == 'right' else -1
            y += 1
            oscillation_waypoints.append((x, y))

    waypoints = diagonal_waypoints + oscillation_waypoints
    return waypoints
