import random

import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self,  bg_img_width, window_height, enemy_size):
        super().__init__()

        self.bg_img_width = bg_img_width
        self.window_height = window_height
        self.enemy_size = enemy_size

        if enemy_size == "sm":
            self.enemy_sm_1 = pygame.image.load("assets/img/enemy/enemy-small_a.png").convert_alpha()
            self.enemy_sm_2 = pygame.image.load("assets/img/enemy/enemy-small_b.png").convert_alpha()
            self.enemy_frames = [self.enemy_sm_1, self.enemy_sm_2]
            self.enemy_index = 0
            self.speed = 2
            self.energy = 20
            self.shot_power = 10
            self.bump_power = 20
            self.shot_score = 6
            self.kill_score = 12
        elif enemy_size == "md":
            self.enemy_md_1 = pygame.image.load("assets/img/enemy/enemy-medium_a.png").convert_alpha()
            self.enemy_md_2 = pygame.image.load("assets/img/enemy/enemy-medium_b.png").convert_alpha()
            self.enemy_frames = [self.enemy_md_1, self.enemy_md_2]
            self.enemy_index = 0
            self.speed = 1
            self.energy = 40
            self.shot_power = 20
            self.bump_power = 40
            self.shot_score = 12
            self.kill_score = 24
        elif enemy_size == "lg":
            self.enemy_lg_1 = pygame.image.load("assets/img/enemy/enemy-big_a.png").convert_alpha()
            self.enemy_lg_2 = pygame.image.load("assets/img/enemy/enemy-big_b.png").convert_alpha()
            self.enemy_frames = [self.enemy_lg_1, self.enemy_lg_2]
            self.enemy_index = 0
            self.speed = 1
            self.energy = 50
            self.shot_power = 40
            self.bump_power = 60
            self.shot_score = 24
            self.kill_score = 48

        self.image = self.enemy_frames[self.enemy_index]
        self.rect = self.image.get_rect(center=(random.randint(10, 250), -5))

    def animate(self):
        self.enemy_index += 0.5
        if self.enemy_index >= len(self.enemy_frames):
            self.enemy_index = 0
        self.image = self.enemy_frames[int(self.enemy_index)]

    def movement(self):
        self.rect.bottom += self.speed

    def destroy(self):
        self.kill()

    def kill_off_screen(self):
        if self.rect.top > self.window_height:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.kill_off_screen()
