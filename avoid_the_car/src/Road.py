import pygame
import time


class Road:
    """Endless scrolling, TOPDOWN [ top to bottom ]"""

    def __init__(self, screen, window_height):

        self.screen = screen
        self.window_height = window_height

        self.image = pygame.image.load("img/road.png").convert_alpha()
        self.image_height = self.image.get_height()

        self.scroll = 0
        self.speed = 70
        self.start_time = time.time()

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
        if levels_data and f"level{level}" in levels_data:
            level_info = levels_data[f"level{level}"]
            self.scroll += level_info["scroll"]
            self.speed = level_info["speed"]

    def update(self, level, levels_data):
        self.scrolling()
        self.movement(level, levels_data)
