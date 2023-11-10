import math
import random

import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, bg_img_width, window_height, enemy_size, player_rect, enemy_speeds):
        super().__init__()

        self.screen = screen
        self.bg_img_width = bg_img_width
        self.window_height = window_height
        self.enemy_size = enemy_size
        self.player_rect = player_rect
        self.enemy_speeds = enemy_speeds

        if enemy_size == "sm1":
            self.enemy_sm1_1 = pygame.image.load("assets/img/enemy/enemy-small_A1.png").convert_alpha()
            self.enemy_sm1_2 = pygame.image.load("assets/img/enemy/enemy-small_A2.png").convert_alpha()
            self.enemy_frames = [self.enemy_sm1_1, self.enemy_sm1_2]
            self.enemy_index = 0
            self.energy = 10
            self.bump_power = 20
            self.shot_score = 6
            self.kill_score = 12
            self.can_shoot = True
        elif enemy_size == "sm2":
            self.enemy_sm2_1 = pygame.image.load("assets/img/enemy/enemy-small_B1.png").convert_alpha()
            self.enemy_sm2_2 = pygame.image.load("assets/img/enemy/enemy-small_B2.png").convert_alpha()
            self.enemy_frames = [self.enemy_sm2_1, self.enemy_sm2_2]
            self.enemy_index = 0
            self.energy = 10
            self.bump_power = 20
            self.shot_score = 6
            self.kill_score = 12
            self.can_shoot = False
        elif enemy_size == "md":
            self.enemy_md_1 = pygame.image.load("assets/img/enemy/enemy-medium_A1.png").convert_alpha()
            self.enemy_md_2 = pygame.image.load("assets/img/enemy/enemy-medium_A2.png").convert_alpha()
            self.enemy_frames = [self.enemy_md_1, self.enemy_md_2]
            self.enemy_index = 0
            self.energy = 20
            self.bump_power = 40
            self.shot_score = 12
            self.kill_score = 24
            self.can_shoot = True
        elif enemy_size == "lg":
            self.enemy_lg_1 = pygame.image.load("assets/img/enemy/enemy-big_A1.png").convert_alpha()
            self.enemy_lg_2 = pygame.image.load("assets/img/enemy/enemy-big_A2.png").convert_alpha()
            self.enemy_frames = [self.enemy_lg_1, self.enemy_lg_2]
            self.enemy_index = 0
            self.energy = 30
            self.bump_power = 60
            self.shot_score = 24
            self.kill_score = 48
            self.can_shoot = True

        self.speed = self.enemy_speeds[self.enemy_size]
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

        if cur_time - self.last_shot_time >= shot_timing and self.can_shoot:
            dx = self.player_rect.centerx - self.rect.centerx
            dy = self.player_rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            direction = (dx / distance, dy / distance)

            shot = EnemyShot("normal", self.rect.midbottom, self.window_height, self.bg_img_width, direction)
            self.shots.add(shot)
            self.last_shot_time = cur_time

    def deduct_energy(self, player_shot_power):
        self.energy -= player_shot_power

    def kill_off_screen(self):
        if self.rect.top > self.window_height * 2:
            self.kill()

    def dead(self):
        if self.energy <= 0:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.kill_off_screen()
        self.shoot()
        self.shots.update()
        self.shots.draw(self.screen)
        self.dead()


class Boss(pygame.sprite.Sprite):
    def __init__(self, screen, bg_img_width, window_height, player_rect, *args):
        super().__init__(*args)

        self.screen = screen
        self.bg_img_width = bg_img_width
        self.window_height = window_height
        self.player_rect = player_rect

        self.boss_img_1 = pygame.image.load("assets/img/boss/boss_1.png").convert_alpha()
        self.boss_img_2 = pygame.image.load("assets/img/boss/boss_2.png").convert_alpha()
        self.boss_frames = [self.boss_img_1, self.boss_img_2]
        self.boss_index = 0
        self.image = self.boss_frames[self.boss_index]
        self.rect = self.image.get_rect(center=(self.bg_img_width // 2, 10))

        self.energy = 300
        self.shot_power = 25
        self.bump_power = 60
        self.shot_score = 48
        self.kill_score = 5000
        self.can_shoot = True

        self.direction = 1
        self.vert_speed = 1

        self.shots = pygame.sprite.Group()
        self.last_shot_time = pygame.time.get_ticks()

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

    def shoot(self):
        cur_time = pygame.time.get_ticks()
        shot_timing = random.randint(800, 1800)

        if cur_time - self.last_shot_time >= shot_timing and self.can_shoot:
            dx = self.player_rect.x - self.rect.x
            dy = self.player_rect.y - self.rect.y

            # Calculate the angle to the player for each bullet
            angle = math.atan2(dy, dx)

            # Calculate the direction vectors for each bullet based on the angles
            direction = (math.cos(angle), math.sin(angle))

            # Create two bullets with their respective directions
            shot = EnemyShot("boss", self.rect.center, self.window_height, self.bg_img_width, direction)

            self.shots.add(shot)
            self.last_shot_time = cur_time

    def deduct_energy(self, player_shot_power):
        self.energy -= player_shot_power

    def dead(self):
        if self.energy <= 0:
            self.kill()
            self.shots.empty()

    def update(self):
        self.animate()
        self.movement()
        self.shoot()
        self.dead()
        self.shots.draw(self.screen)
        self.shots.update()


class EnemyShot(pygame.sprite.Sprite):
    def __init__(self, shot_type, placement, window_width, window_height, direction):
        super().__init__()

        self.shot_type = shot_type
        self.placement = placement  # rect tuple
        self.window_width = window_width
        self.window_height = window_height
        self.direction = direction

        if shot_type == "normal":
            self.shot_ball_1 = pygame.image.load("assets/img/shot/shot_ball_1.png").convert_alpha()
            self.shot_ball_2 = pygame.image.load("assets/img/shot/shot_ball_2.png").convert_alpha()
            self.shot_ball_3 = pygame.image.load("assets/img/shot/shot_ball_3.png").convert_alpha()
            self.bullet_frames = [self.shot_ball_1, self.shot_ball_2, self.shot_ball_3]
        elif shot_type == "boss":
            self.boss_shot_1 = pygame.image.load("assets/img/shot/boss_shot_1.png").convert_alpha()
            self.boss_shot_2 = pygame.image.load("assets/img/shot/boss_shot_2.png").convert_alpha()
            self.boss_shot_3 = pygame.image.load("assets/img/shot/boss_shot_3.png").convert_alpha()
            self.bullet_frames = [self.boss_shot_1, self.boss_shot_2, self.boss_shot_3]
        self.bullet_index = 0

        self.image = self.bullet_frames[self.bullet_index]
        self.rect = self.image.get_rect(midbottom=self.placement)
        self.rect.x -= 1

    def animate(self):
        self.bullet_index += 0.5
        if self.bullet_index >= len(self.bullet_frames):
            self.bullet_index = 0
        self.image = self.bullet_frames[int(self.bullet_index)]

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
