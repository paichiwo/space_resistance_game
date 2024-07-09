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