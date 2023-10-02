import pygame
import random


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("img/enemy.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 180, 2)
        self.rect = self.image.get_rect(midbottom=(random.randint(170, 410), 0))

    def movement(self, increase, acceleration):
        self.rect.y += 6
        if self.rect.y >= 800:
            self.rect.midbottom = (random.randint(170, 410), 0)
        if increase:
            self.rect.y += 3 + acceleration

    def update(self, increase, acceleration):
        self.movement(increase, acceleration)
