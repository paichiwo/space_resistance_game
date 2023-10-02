import pygame
import math
import time


class Road:
    """Endless scrolling, TOPDOWN [ top to bottom ]"""

    def __init__(self, screen, window_height, font):

        self.screen = screen
        self.window_height = window_height
        self.font = font

        self.image = pygame.image.load("img/road.png").convert_alpha()
        self.image_height = self.image.get_height()

        self.scroll = 0
        self.panels = math.ceil(self.window_height / self.image_height + 2)

        self.acc = 0
        self.speed = 70
        self.min_speed = 70
        self.max_speed = 160
        self.increase = False
        self.decrease = False
        self.distance = 0
        self.start_time = time.time()

    def scrolling(self):
        """Endless scroll method"""
        self.scroll += 4
        for i in range(self.panels):
            y_pos = int((i * self.image_height) + self.scroll - self.image_height)
            self.screen.blit(self.image, (0, y_pos))
            if abs(self.scroll) >= self.image_height:
                self.scroll = 0

    def update_speed(self):
        """Adjust road speed based on player input"""
        if self.increase:
            self.speed += 1.5
        elif self.decrease:
            self.speed -= 1
        self.speed = int(max(self.min_speed, min(self.max_speed, self.speed)))

    def update_distance(self):
        """Count distance based on time and speed"""
        current_time = time.time()
        delta_time = current_time - self.start_time
        delta_time_seconds = delta_time * 0.000278
        delta_distance = self.speed * delta_time_seconds + (self.acc * delta_time_seconds ** 2) / 2
        self.distance += delta_distance
        self.start_time = current_time

    def movement(self):
        """Adjust scrolling speed based on user input"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
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

    def update(self):
        self.scrolling()
        self.movement()
        self.update_speed()
        self.update_distance()
