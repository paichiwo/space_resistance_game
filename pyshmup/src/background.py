import pygame
import math


class Background:
    """Creates a background object"""
    def __init__(self, screen, window_height):

        self.screen = screen
        self.window_height = window_height

        self.bg_1 = pygame.image.load("assets/img/bg/space/space-background.png").convert_alpha()
        self.bg_2 = pygame.image.load("assets/img/bg/desert/desert-background.png").convert_alpha()
        self.bg_3 = pygame.image.load("assets/img/bg/river/river-background.png").convert_alpha()
        self.level_images = [self.bg_1, self.bg_2, self.bg_3]
        self.level_index = 0
        self.bg = self.level_images[self.level_index]
        self.panels = self.get_panels()

        self.scroll = 0
        self.speed = 0.5
        self.scroll_count = 0

    def get_panels(self):
        return math.ceil(self.window_height / self.bg.get_height() + 1)

    def scrolling(self):
        """Endless scroll method"""
        for i in range(self.panels):
            y_pos = int((i * self.bg.get_height()) + self.scroll - self.bg.get_height())
            self.screen.blit(self.bg, (0, y_pos))
            if abs(self.scroll) >= self.bg.get_height():
                self.scroll = 0
                self.count_scrolls()
        self.scroll += self.speed

    def count_scrolls(self):
        self.scroll_count += 1
        return self.scroll_count

    def change_bg(self, level):
        if 1 <= level <= len(self.level_images):
            self.bg = self.level_images[level-1]
            self.panels = self.get_panels()
            self.scroll_count = 0

    def update(self):
        self.scrolling()
