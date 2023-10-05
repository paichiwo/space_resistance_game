import pygame
from avoid_the_car.src.utils import get_level_info


class Player(pygame.sprite.Sprite):
    """Creates a player object."""

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(midbottom=(300, 700))

        self.speed = 70

    def movement(self):
        """Move the player's car left or right based on user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3

    def stay_on_road(self):
        """Keep the player's car within road boundaries."""
        if self.rect.x >= 390:
            self.rect.x -= 10
        if self.rect.x <= 160:
            self.rect.x += 10

    def update_speed(self, level, levels_data):
        """Update player's speed"""
        level_info = get_level_info(level, levels_data)
        self.speed = level_info["speed"]

    def update(self, level, levels_data):
        self.movement()
        self.stay_on_road()
        self.update_speed(level, levels_data)
