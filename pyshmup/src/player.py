import time

import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, bg_img_width, window_height, *args):
        super().__init__(*args)

        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.ship_mid = pygame.image.load("assets/img/ship/middle.png").convert_alpha()
        self.ship_left_1 = pygame.image.load("assets/img/ship/left_1.png").convert_alpha()
        self.ship_left_2 = pygame.image.load("assets/img/ship/left_2.png").convert_alpha()
        self.left_frames = [self.ship_left_1, self.ship_left_2]
        self.left_index = 0

        self.ship_right_1 = pygame.image.load("assets/img/ship/right_1.png").convert_alpha()
        self.ship_right_2 = pygame.image.load("assets/img/ship/right_2.png").convert_alpha()

        self.fumes_1 = pygame.image.load("assets/img/ship/fumes_1.png")
        self.fumes_2 = pygame.image.load("assets/img/ship/fumes_2.png")
        self.fumes_frames = [self.fumes_1, self.fumes_2]
        self.fumes_index = 0

        self.image = None
        self.rect = None

        self.fumes_image = None
        self.fumes_rect = None

        self.render()

    def render(self):
        """Render player image"""
        self.image = self.ship_mid
        self.rect = self.image.get_rect(midbottom=(self.bg_img_width / 2, self.window_height - 10))

    def animate_fumes(self):
        self.fumes_index += 0.8
        if self.fumes_index >= len(self.fumes_frames):
            self.fumes_index = 0
        self.image = self.fumes_frames[int(self.fumes_index)]

    def animate_left_(self):
        self.left_index += 0.01
        if self.left_index >= len(self.left_frames):
            self.left_index = 1
        self.image = self.left_frames[int(self.left_index)]

    def movement(self):
        """Rules for moving the player"""

        self.animate_mid()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.rect.y -= 2

        if keys[pygame.K_DOWN]:
            self.rect.y += 2

        if keys[pygame.K_LEFT]:
            self.rect.x -= 2

        if keys[pygame.K_RIGHT]:
            self.rect.x += 2

    def update(self):
        self.movement()
