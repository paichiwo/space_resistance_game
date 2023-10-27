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

        if enemy_size == "sm1":
            self.enemy_sm1_1 = pygame.image.load("assets/img/enemy/enemy-small_A1.png").convert_alpha()
            self.enemy_sm1_2 = pygame.image.load("assets/img/enemy/enemy-small_A2.png").convert_alpha()
            self.enemy_frames = [self.enemy_sm1_1, self.enemy_sm1_2]
            self.enemy_index = 0
            self.speed = 2
            self.energy = 20
            self.bump_power = 20
            self.shot_score = 6
            self.kill_score = 12
            self.can_shoot = False
        elif enemy_size == "sm2":
            self.enemy_sm2_1 = pygame.image.load("assets/img/enemy/enemy-small_B1.png").convert_alpha()
            self.enemy_sm2_2 = pygame.image.load("assets/img/enemy/enemy-small_B2.png").convert_alpha()
            self.enemy_frames = [self.enemy_sm2_1, self.enemy_sm2_2]
            self.enemy_index = 0
            self.speed = 2
            self.energy = 20
            self.bump_power = 20
            self.shot_score = 6
            self.kill_score = 12
            self.can_shoot = True
        elif enemy_size == "md":
            self.enemy_md_1 = pygame.image.load("assets/img/enemy/enemy-medium_A1.png").convert_alpha()
            self.enemy_md_2 = pygame.image.load("assets/img/enemy/enemy-medium_A2.png").convert_alpha()
            self.enemy_frames = [self.enemy_md_1, self.enemy_md_2]
            self.enemy_index = 0
            self.speed = 1
            self.energy = 40
            self.bump_power = 40
            self.shot_score = 12
            self.kill_score = 24
            self.can_shoot = True
        elif enemy_size == "lg":
            self.enemy_lg_1 = pygame.image.load("assets/img/enemy/enemy-big_A1.png").convert_alpha()
            self.enemy_lg_2 = pygame.image.load("assets/img/enemy/enemy-big_A2.png").convert_alpha()
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
        shot_timing = random.randint(800, 1800)
        if self.can_shoot:
            if cur_time - self.last_shot_time >= shot_timing:

                dx = self.player_rect.centerx - self.rect.centerx
                dy = self.player_rect.centery - self.rect.centery
                distance = math.sqrt(dx * dx + dy * dy)
                direction = (dx / distance, dy / distance)

                shot = EnemyShot(self.rect, self.window_height, self.bg_img_width, direction)
                self.shots.add(shot)
                self.last_shot_time = cur_time

    def deduct_energy(self, player_shot_power):
        self.energy -= player_shot_power

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

        self.shot_ball_1 = self.image = pygame.image.load("assets/img/shot/shot_ball_a.png")
        self.shot_ball_2 = self.image = pygame.image.load("assets/img/shot/shot_ball_b.png")
        self.shot_ball_frames = [self.shot_ball_1, self.shot_ball_2]
        self.shot_ball_index = 0

        self.image = self.shot_ball_frames[self.shot_ball_index]
        self.rect = self.image.get_rect(midbottom=enemy_rect.midbottom)
        self.rect.x -= 1

    def animate(self):
        self.shot_ball_index += 0.5
        if self.shot_ball_index >= len(self.shot_ball_frames):
            self.shot_ball_index = 0
        self.image = self.shot_ball_frames[int(self.shot_ball_index)]

    def movement(self):
        self.rect.x += self.direction[0] * 3
        self.rect.y += self.direction[1] * 3

    def kill_off_screen(self):
        if self.rect.top > self.window_height or self.rect.bottom < 0 or self.rect.right < 0 or self.rect.left > self.window_width:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.kill_off_screen()
