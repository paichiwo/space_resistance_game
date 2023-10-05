import pygame
from avoid_the_car.src.utils import get_level_info


class Road:
    """Endless scrolling, TOPDOWN [ top to bottom ]"""

    def __init__(self, screen, window_height):

        self.screen = screen
        self.window_height = window_height

        self.image = pygame.image.load("img/road.png").convert_alpha()
        self.image_height = self.image.get_height()

        self.scroll = 0

    def scrolling(self):
        """Endless scroll method"""
        self.scroll += 4
        if self.scroll >= self.image_height:
            self.scroll = 0
        blit_offset = self.scroll % self.image_height
        self.screen.blit(self.image, (0, blit_offset))
        self.screen.blit(self.image, (0, blit_offset - self.image_height))

    def movement(self, level, levels_data):
        """Adjust scrolling speed based on user input"""
        level_info = get_level_info(level, levels_data)
        self.scroll += level_info["scroll"]

    def update(self, level, levels_data):
        self.scrolling()
        self.movement(level, levels_data)
