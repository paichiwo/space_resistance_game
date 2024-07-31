import pygame.gfxdraw

from src.config import *
import math
import sys
from src.helpers import circular_waypoints, generate_sine_wave_waypoints


class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, group):
        super().__init__(group)

        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.waypoints = waypoints
        self.current_waypoint = 0
        self.speed = 2

        if waypoints:
            self.rect.center = waypoints[0]

    def update(self):
        if self.current_waypoint < len(self.waypoints):
            target_x, target_y = self.waypoints[self.current_waypoint]
            dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
            dist = math.hypot(dx, dy)

            if dist != 0:
                dx, dy = dx / dist, dy / dist
                self.rect.x += dx * self.speed
                self.rect.y += dy * self.speed

            if dist < self.speed:
                self.current_waypoint += 1


class Game:
    def __init__(self):
        pygame.init()
        self.s_width, self.s_height = 255, 480
        self.screen = pygame.display.set_mode((self.s_width, self.s_height))
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.waypoints = circular_waypoints(self.s_width, self.s_height)


        self.enemy_spawn_time = 300
        self.last_spawn_time = pygame.time.get_ticks()
        self.enemies_to_spawn = 8

    def spawn_enemy(self, waypoints):
        Enemy(waypoints, [self.enemies, self.all_sprites])

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            if self.enemies_to_spawn > 0 and current_time - self.last_spawn_time >= self.enemy_spawn_time:
                Enemy(self.waypoints, [self.enemies, self.all_sprites])
                self.last_spawn_time = current_time
                self.enemies_to_spawn -= 1

            self.all_sprites.update()
            self.screen.fill('black')
            self.all_sprites.draw(self.screen)
            pygame.draw.aalines(self.screen, 'blue', False, self.waypoints)

            pygame.display.flip()

            self.clock.tick(60)


if __name__ == '__main__':
    Game().run()
