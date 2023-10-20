import math
import random

import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, bg_img_width, window_height, enemy_size, player_rect):
        super().__init__()

        self.screen = screen
        self.bg_img_width = bg_img_width
        self.window_height = window_height
        self.enemy_size = enemy_size
        self.player_rect = player_rect

        if enemy_size == "sm":
            self.enemy_sm_1 = pygame.image.load("assets/img/enemy/enemy-small_a.png").convert_alpha()
            self.enemy_sm_2 = pygame.image.load("assets/img/enemy/enemy-small_b.png").convert_alpha()
            self.enemy_frames = [self.enemy_sm_1, self.enemy_sm_2]
            self.enemy_index = 0
            self.speed = 2
            self.energy = 20
            self.bump_power = 20
            self.shot_score = 6
            self.kill_score = 12
            self.can_shoot = False
        elif enemy_size == "md":
            self.enemy_md_1 = pygame.image.load("assets/img/enemy/enemy-medium_a.png").convert_alpha()
            self.enemy_md_2 = pygame.image.load("assets/img/enemy/enemy-medium_b.png").convert_alpha()
            self.enemy_frames = [self.enemy_md_1, self.enemy_md_2]
            self.enemy_index = 0
            self.speed = 1
            self.energy = 40
            self.bump_power = 40
            self.shot_score = 12
            self.kill_score = 24
            self.can_shoot = True
        elif enemy_size == "lg":
            self.enemy_lg_1 = pygame.image.load("assets/img/enemy/enemy-big_a.png").convert_alpha()
            self.enemy_lg_2 = pygame.image.load("assets/img/enemy/enemy-big_b.png").convert_alpha()
            self.enemy_frames = [self.enemy_lg_1, self.enemy_lg_2]
            self.enemy_index = 0
            self.speed = 1
            self.energy = 50
            self.bump_power = 60
            self.shot_score = 24
            self.kill_score = 48
            self.can_shoot = True

        self.shot_power = 20

        self.shots = pygame.sprite.Group()
        self.shot_delay = 1000
        self.last_shot_time = pygame.time.get_ticks()

        self.image = self.enemy_frames[self.enemy_index]
        self.rect = self.image.get_rect(center=(random.randint(10, 250), -5))

    def animate(self):
        self.enemy_index += 0.5
        if self.enemy_index >= len(self.enemy_frames):
            self.enemy_index = 0
        self.image = self.enemy_frames[int(self.enemy_index)]

    def movement(self):
        self.rect.bottom += self.speed

    def shoot(self):
        cur_time = pygame.time.get_ticks()
        if self.can_shoot:
            if cur_time - self.last_shot_time >= self.shot_delay:

                dx = self.player_rect.centerx - self.rect.centerx
                dy = self.player_rect.centery - self.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                direction = (dx / distance, dy / distance)

                shot = EnemyShot(self.rect, self.window_height, self.bg_img_width, direction)
                self.shots.add(shot)
                self.last_shot_time = cur_time

    def destroy(self):
        self.kill()

    def kill_off_screen(self):
        if self.rect.top > self.window_height * 2:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.kill_off_screen()
        self.shoot()
        self.shots.update()
        self.shots.draw(self.screen)


class EnemyShot(pygame.sprite.Sprite):
    def __init__(self, enemy_rect, window_width, window_height, direction):
        super().__init__()

        self.window_width = window_width
        self.window_height = window_height
        self.direction = direction

        self.image = pygame.image.load("assets/img/shot/shot_ball_b.png")
        self.rect = self.image.get_rect(midbottom=enemy_rect.midbottom)
        self.rect.x -= 1

    def movement(self):
        self.rect.x += self.direction[0] * 3
        self.rect.y += self.direction[1] * 3

    def kill_off_screen(self):
        if self.rect.top > self.window_height or self.rect.bottom < 0 or self.rect.left > self.window_width or self.rect.right < 0:
            self.kill()

    def update(self):
        self.movement()
        self.kill_off_screen()
