import pygame
import math


class Background:
    """Creates a background object"""
    def __init__(self, screen, window_height):

        self.screen = screen
        self.window_height = window_height

        self.bg_1 = pygame.image.load("assets/img/bg/desert/desert-background.png").convert_alpha()
        self.img_height = self.bg_1.get_height()
        self.panels = math.ceil(self.window_height / self.img_height + 2)
        self.scroll = 0

    def scrolling(self):
        """Endless scroll method"""
        for i in range(self.panels):
            y_pos = int((i * self.img_height) + self.scroll - self.img_height)
            self.screen.blit(self.bg_1, (0, y_pos))
            if abs(self.scroll) >= self.img_height:
                self.scroll = 0
        self.scroll += 1

    def update(self):
        self.scrolling()
