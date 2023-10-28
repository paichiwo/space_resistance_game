import pygame
import math
import time


class Road:
    """Endless scrolling, TOPDOWN [ top to bottom ]"""

    def __init__(self, screen, window_height):

        self.screen = screen
        self.window_height = window_height

        self.image = pygame.image.load("img/road.png").convert_alpha()
        self.image_height = self.image.get_height()

        self.scroll = 0
        self.acc = 0
        self.speed = 70
        self.min_speed = 70
        self.max_speed = 160
        self.increase = False
        self.decrease = False
        self.start_time = time.time()

    def scrolling(self):
        """Endless scroll method"""
        self.scroll += 4
        if self.scroll >= self.image_height:
            self.scroll = 0

        blit_offset = self.scroll % self.image_height
        self.screen.blit(self.image, (0, blit_offset))
        self.screen.blit(self.image, (0, blit_offset - self.image_height))

    def update_speed(self):
        """Adjust road speed based on player input"""
        if self.increase:
            self.speed += 1.5
        elif self.decrease:
            self.speed -= 1
        self.speed = int(max(self.min_speed, min(self.max_speed, self.speed)))

    def movement(self, level):
        """Adjust scrolling speed based on user input"""
        if level == 1:
            self.acc += 0.15
            self.increase = True
            self.decrease = False
            # don't speed forever
            self.acc = min(self.acc, 9)
        else:
            # Gradually reduce acceleration when no UP key is pressed
            if self.acc > 0:
                self.acc -= 0.1  # rate of decrease
                self.speed -= 3
                self.increase = True
                self.decrease = False
                if self.scroll <= 0.02:
                    self.scroll = 0
            elif self.acc < 0:
                self.decrease = True
                self.increase = False

        self.scroll += self.acc

    def update(self, level):
        self.scrolling()
        self.movement(level)
        self.update_speed()
