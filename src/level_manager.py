import math
import random
import pygame._sdl2 as sdl2
from src.config import *
from src.helpers import import_assets
from src.timer import Timer
from src.dashboard import Dashboard
from src.player import Player
from src.enemy import Enemy
from src.messages import MessageBetweenLevels


class LevelManager:
    def __init__(self, screen, renderer, sound_manager):
        self.screen = screen
        self.renderer = renderer
        self.sound_manager = sound_manager

        # Background
        self.level_images = import_assets('assets/img/bg/')
        self.level_index = 0
        self.bg_img = self.level_images[self.level_index]
        self.panels = self.get_panels()

        self.scroll_pos = 0
        self.scroll_speed = 60
        self.scroll_count = 0

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Objects
        self.player = Player(self.screen, self.sound_manager, self.enemy_sprites, self.all_sprites)
        self.dashboard = Dashboard(self.screen, self.player)

        # Timers
        self.enemy_spawn_timer = None
        self.set_enemy_spawn_timer()

        # Message display state
        self.showing_level_message = False
        self.message_start_time = None

    def get_panels(self):
        return math.ceil(HEIGHT / self.bg_img.get_height() + 1)

    def scroll(self, dt):
        for i in range(self.panels):
            y_pos = int((i * self.bg_img.get_height()) + self.scroll_pos - self.bg_img.get_height())
            self.screen.blit(self.bg_img, (0, y_pos))
        if abs(self.scroll_pos) >= self.bg_img.get_height():
            self.scroll_pos = 0
            self.count_scrolls()
        self.scroll_pos += self.scroll_speed * dt

    def start_scrolling(self):
        self.scroll_speed = 60

    def stop_scrolling(self):
        self.scroll_speed = 0
        self.scroll_pos = 0

    def count_scrolls(self):
        self.scroll_count += 1
        return self.scroll_count

    def change_bg(self, level):
        if 1 <= level <= len(self.level_images) and not level == 4:
            self.bg_img = self.level_images[level]
            self.panels = self.get_panels()
            self.scroll_count = 0

    def set_levels(self):
        if self.scroll_count == 1 and not self.level_index == 3:
            self.level_index += 1
            self.finish_level()
            self.change_bg(self.level_index)
            if self.level_index == 3:
                self.spawn_boss()

    def finish_level(self):
        self.stop_scrolling()
        self.message_start_time = pygame.time.get_ticks()
        self.showing_level_message = True

    def show_level_message(self):
        message = [f'LEVEL {self.level_index + 1}', f'ENEMY KILLS: {self.player.enemy_kill_count}']
        MessageBetweenLevels(self.screen, message).show()
        sdl2.Texture.from_surface(self.renderer, self.screen).draw()
        self.renderer.present()

    def start_new_level(self):
        self.scroll_pos = 0
        self.scroll_count = 0
        self.all_sprites.remove(sprite for sprite in self.enemy_sprites if sprite in self.all_sprites)
        self.enemy_sprites.empty()
        self.player.shots_group.empty()
        self.player.enemy_kill_count = 0
        self.start_scrolling()

    def between_levels(self):
        self.sound_manager.stop_all_music()
        current_time = pygame.time.get_ticks()
        if current_time - self.message_start_time < 3000:
            self.show_level_message()
        else:
            self.showing_level_message = False
            self.start_new_level()

    def set_enemy_spawn_timer(self):
        level = str(self.level_index + 1)
        if level in ENEMY_LEVEL_DATA:
            interval_range = ENEMY_LEVEL_DATA[level]['spawning_intervals']
            interval = random.randint(interval_range[0], interval_range[1])
            self.enemy_spawn_timer = Timer(interval, self.spawn_enemy, repeat=True, autostart=True)

    def spawn_enemy(self):
        level = str(self.level_index + 1)
        if level in ENEMY_LEVEL_DATA:
            choices = [entry['choice'] for entry in ENEMY_LEVEL_DATA[level]['choices']]
            probabilities = [entry['probability'] for entry in ENEMY_LEVEL_DATA[level]['choices']]
            enemy_choice = random.choices(choices, probabilities)[0]
            Enemy(self.screen, self.sound_manager, self.player, enemy_choice,
                  level, [self.enemy_sprites, self.all_sprites])

    def spawn_boss(self):
        pass

    def restart(self):
        self.level_index = 0
        self.bg_img = self.level_images[0]
        self.scroll_count = 0
        self.scroll_pos = 0
        self.enemy_sprites.empty()
        self.player.reset()

    def update(self, dt):
        if self.showing_level_message:
            self.between_levels()
        else:
            self.scroll(dt)
            self.all_sprites.draw(self.screen)
            self.all_sprites.update(dt)
            self.dashboard.update(self.player, self.level_index, dt)
            self.enemy_spawn_timer.update()
            self.set_levels()
