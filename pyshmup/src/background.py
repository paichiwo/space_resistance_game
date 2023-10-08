import pygame
import math


class Background:

    def __init__(self, screen, window_height):

        self.screen = screen
        self.window_height = window_height

        self.bg_1 = pygame.image.load("assets/img/bg/desert/desert-background.png").convert_alpha()
        self.image_height = self.bg_1.get_height()
        self.scroll = 0

    def scrolling(self):
        """Endless scroll method"""
        panels = math.ceil(self.window_height / self.image_height + 2)

        self.scroll += 1
        for i in range(panels):
            y_pos = int((i * self.image_height) + self.scroll - self.image_height)
            self.screen.blit(self.bg_1, (0, y_pos))
            if abs(self.scroll) >= self.image_height:
                self.scroll = 0

    def update(self):
        self.scrolling()
