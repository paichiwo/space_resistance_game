import sys
import math
import pygame._sdl2 as sdl2
from src.config import *
from src.helpers import circular_path, sine_wave_path, diagonal_path, down_and_oscillate_path


class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, group):
        super().__init__(group)

        self.image = pygame.Surface((15, 15))
        self.image.fill((255, 0, 0))

        self.pos = pygame.math.Vector2(waypoints[0])
        self.rect = self.image.get_frect(center=self.pos)

        self.waypoints = waypoints
        self.current_waypoint = 0
        self.speed = 100

        if waypoints:
            self.rect.center = waypoints[0]

    def move(self, dt):
        if self.current_waypoint < len(self.waypoints):
            target_x, target_y = self.waypoints[self.current_waypoint]
            dx, dy = target_x - self.pos.x, target_y - self.pos.y
            dist = math.hypot(dx, dy)

            if dist > 0:
                direction = pygame.math.Vector2(dx, dy).normalize()
                self.pos += direction * self.speed * dt

                self.rect.center = (self.pos.x, self.pos.y)

            if dist < self.speed * dt:
                self.current_waypoint += 1

    def update(self, dt):
        self.move(dt)


class Game:
    def __init__(self):
        pygame.init()
        self.s_width, self.s_height = 216, 250
        self.clock = pygame.time.Clock()

        self.scale = 4
        self.window = pygame.Window(size=(WIDTH * self.scale, HEIGHT * self.scale), title='Paths Test')
        self.window.resizable = True
        self.renderer = sdl2.Renderer(self.window, accelerated=True)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()

        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        self.waypoints_dict = {
            'circular left': circular_path(self.s_width, self.s_height, direction='left'),
            'circular right': circular_path(self.s_width, self.s_height, direction='right'),
            'sinus left': sine_wave_path(self.s_width, self.s_height, direction='left'),
            'sinus right': sine_wave_path(self.s_width, self.s_height, direction='right'),
            'line left': diagonal_path(self.s_width, self.s_height, direction='left'),
            'line right': diagonal_path(self.s_width, self.s_height, direction='right'),
            'down oscillation': down_and_oscillate_path(self.s_width, self.s_height, y_pos=160)
        }
        self.waypoints_index = 0
        self.waypoints_keys = list(self.waypoints_dict.keys())
        self.current_waypoint_name = self.waypoints_keys[self.waypoints_index]

        self.enemy_spawn_time = 500
        self.last_spawn_time = pygame.time.get_ticks()
        self.enemies_to_spawn = 8

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.waypoints_index = (self.waypoints_index - 1) % len(self.waypoints_keys)
                self.change_waypoint()
            elif event.key == pygame.K_RIGHT:
                self.waypoints_index = (self.waypoints_index + 1) % len(self.waypoints_keys)
                self.change_waypoint()

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()

        if self.enemies_to_spawn > 0 and current_time - self.last_spawn_time >= self.enemy_spawn_time:
            waypoints = self.waypoints_dict[self.current_waypoint_name]
            Enemy(waypoints, [self.enemies, self.all_sprites])
            self.last_spawn_time = current_time
            self.enemies_to_spawn -= 1

    def change_waypoint(self):
        self.all_sprites.empty()
        self.enemies.empty()
        self.enemies_to_spawn = 8
        self.last_spawn_time = pygame.time.get_ticks()
        self.current_waypoint_name = self.waypoints_keys[self.waypoints_index]

    def draw_waypoints_path(self):
        pygame.draw.aalines(self.screen, 'blue', False, self.waypoints_dict[self.current_waypoint_name])

    def draw_waypoint_name(self):
        text = FONT20.render(self.current_waypoint_name, True, 'white')
        rect = text.get_rect(center=(self.s_width // 2, self.s_height - 20))
        self.screen.blit(text, rect)

    def run(self):
        while self.running:
            self.screen.fill('black')
            self.renderer.clear()

            for event in pygame.event.get():
                self.handle_events(event)

            dt = self.clock.tick() / 1000

            self.spawn_enemy()

            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)

            self.draw_waypoints_path()
            self.draw_waypoint_name()

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()


if __name__ == '__main__':
    Game().run()
