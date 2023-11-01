import pygame
from math import radians, sin, cos, pi


class Boss(pygame.sprite.Sprite):
    def __init__(self, bg_img_width, window_height, *args):
        super().__init__(*args)

        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.boss_img_1 = pygame.image.load("assets/img/boss/boss_1.png").convert_alpha()
        self.boss_img_2 = pygame.image.load("assets/img/boss/boss_2.png").convert_alpha()
        self.boss_frames = [self.boss_img_1, self.boss_img_2]
        self.boss_index = 0

        self.energy = 50
        self.bump_power = 60
        self.shot_score = 24
        self.kill_score = 48
        self.can_shoot = True

        self.speed = 1
        self.shot_power = 20

        self.direction = 1
        self.vert_speed = 1

        self.shots = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()

        self.image = self.boss_frames[self.boss_index]
        self.rect = self.image.get_rect(center=(self.bg_img_width // 2, 10))

    def animate(self):
        self.boss_index += 0.5
        if self.boss_index >= len(self.boss_frames):
            self.boss_index = 0
        self.image = self.boss_frames[int(self.boss_index)]

    def movement(self):
        if self.rect.y >= self.window_height - 100:
            self.direction = -1  # Move up when close to the bottom
        elif self.rect.y <= 10:
            self.direction = 1  # Move down when close to the top

        self.rect.y += self.direction * self.vert_speed

    def update(self):
        self.animate()
        self.movement()
