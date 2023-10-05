import time

import pygame
import random


class Obstacle(pygame.sprite.Sprite):
    """Creates obstacle object"""

    def __init__(self, object_type):
        super().__init__()

        if object_type == "car":
            self.bike = pygame.image.load("img/bike_1.png").convert_alpha()
            self.casual = pygame.image.load("img/casual_1.png").convert_alpha()
            self.jeep = pygame.image.load("img/jeep_1.png").convert_alpha()
            self.sport_1 = pygame.image.load("img/sport_1.png").convert_alpha()
            self.sport_2 = pygame.image.load("img/sport_2.png").convert_alpha()

            self.car_images = [self.bike, self.casual, self.jeep, self.sport_1, self.sport_2]
            self.car_index = 0

            self.image = None
            self.rect = None

            self.render_obstacle()

    def render_obstacle(self):
        """Render random obstacle"""
        self.car_index = random.choice([n for n in range(len(self.car_images))])
        self.image = self.car_images[self.car_index]
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(midbottom=(random.randint(180, 410), 0))

    def movement(self, level, levels_data):
        """Rules for obstacle movement"""
        self.rect.y += 7
        if levels_data and f"level{level}" in levels_data:
            level_info = levels_data[f"level{level}"]
            self.rect.y += level_info["scroll"]

    def destroy(self):
        """Destroy off-screen obstacle"""
        if self.rect.y >= 800:
            self.kill()

    def update(self, level, levels_data):
        self.movement(level, levels_data)
        self.destroy()
