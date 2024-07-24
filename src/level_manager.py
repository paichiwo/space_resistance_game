import math
import pygame._sdl2 as sdl2
from src.config import *
from src.helpers import import_assets
from src.dashboard import Dashboard
from src.player import Player
from src.enemy import Enemy, Boss
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
        self.rect = self.bg_img.get_frect()
        self.panels = self.get_panels()

        self.scroll_pos = 0
        self.scroll_speed = OBJECT_SPEEDS['scroll']
        self.scroll_count = 0
        self.total_pos_count = 0
        self.bg_offset = 20

        # Groups
        self.all_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Objects
        self.player = Player(self.screen, self.sound_manager, self.enemy_sprites, self.all_sprites)
        self.dashboard = Dashboard(self.screen, self.player)

        # Timers
        self.start_time = pygame.time.get_ticks()

        # Message display state
        self.showing_level_message = False
        self.message_start_time = None

        # Game over
        self.game_over = False

        # Boss
        self.boss = None
        self.boss_spawned = False
        self.boss_killed = False

    def get_panels(self):
        return math.ceil(HEIGHT / self.bg_img.get_height() + 1)

    def scroll(self, dt):
        """
        #  Infinite looping bg scroll
        #
        #     for i in range(self.panels):
        #         y_pos = int((i * self.bg_img.get_height()) + self.scroll_pos - self.bg_img.get_height())
        #         self.screen.blit(self.bg_img, (-self.bg_offset, y_pos))
        #     if abs(self.scroll_pos) >= self.bg_img.get_height()
        #         self.scroll_pos = 0
        #         self.count_scrolls()
        #     self.scroll_pos += self.scroll_speed * dt
        #     self.total_pos_count += self.scroll_speed * dt
        """

        self.rect.y += self.scroll_speed * dt
        y_pos = self.rect.y - self.bg_img.get_height()
        self.screen.blit(self.bg_img, (-self.bg_offset, y_pos + HEIGHT))
        self.scroll_pos += self.scroll_speed * dt
        if int(self.scroll_pos) >= self.bg_img.get_height() - HEIGHT:
            self.scroll_pos = 0
            self.count_scrolls()
        self.total_pos_count += self.scroll_speed * dt

        print(abs(self.scroll_pos))
        # self.total_pos_count += self.scroll_speed * dt

    def update_bg_offset(self, dt):
        player_direction = self.player.direction.x

        if player_direction != 0:
            self.bg_offset += player_direction * 24 * dt
            self.bg_offset = max(0, min(40, self.bg_offset))

    def start_scrolling(self):
        self.scroll_speed = OBJECT_SPEEDS['scroll']

    def stop_scrolling(self):
        self.scroll_speed = 0
        self.scroll_pos = 0

    def count_scrolls(self):
        self.scroll_count += 1

    def change_bg(self, level):
        if 0 <= level <= len(self.level_images) and not level == 3:
            self.bg_img = self.level_images[level]
            self.panels = self.get_panels()
            self.scroll_count = 0

    def set_levels(self):
        if self.scroll_count == 1 and not self.level_index == 3:
            self.level_index += 1
            self.finish_level()
            self.change_bg(self.level_index)

        if self.level_index == 3 and not self.boss_spawned:
            self.bg_img = self.level_images[2]
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
        self.player.god_mode = False
        self.boss_spawned = False
        self.start_scrolling()

    def between_levels(self):
        self.sound_manager.stop_all_music()
        current_time = pygame.time.get_ticks()
        if current_time - self.message_start_time < 3000:
            self.show_level_message()
        else:
            self.showing_level_message = False
            self.start_new_level()

    def spawn_enemy(self):
        current_time = pygame.time.get_ticks()
        if self.level_index in ENEMY_WAVES:
            for spawn_pos in ENEMY_WAVES[self.level_index].keys():
                wave_info = ENEMY_WAVES[self.level_index][spawn_pos]
                quantity = wave_info['quantity']
                delay = wave_info['delay']

                if current_time - self.start_time >= delay:
                    if round(self.total_pos_count) in range(spawn_pos[0], spawn_pos[1]) and quantity > 0:
                        Enemy(
                            self.screen,
                            self.sound_manager,
                            self.player,
                            wave_info['type'],
                            wave_info['speed'],
                            wave_info['waypoints'],
                            [self.enemy_sprites, self.all_sprites]
                        )
                        self.start_time = current_time
                        quantity -= 1

    def spawn_boss(self):
        self.boss = Boss(self.screen, self.player, self.sound_manager, [self.enemy_sprites, self.all_sprites])
        self.boss_spawned = True

    def game_win_or_game_over(self):
        if self.level_index == 3:
            if self.boss not in self.enemy_sprites:
                self.boss_killed = True

        if self.player.lives <= 0:
            self.game_over = True

    def restart(self):
        self.game_over = False
        self.boss_spawned = False
        self.boss_killed = False
        self.level_index = 0
        self.bg_img = self.level_images[0]
        self.scroll_count = 0
        self.scroll_pos = 0
        self.all_sprites.remove(sprite for sprite in self.enemy_sprites if sprite in self.all_sprites)
        self.enemy_sprites.empty()
        self.player.reset()

    def pause(self):
        for enemy in self.enemy_sprites:
            enemy.speed = 0
            for shot in enemy.shots_group:
                shot.speed = 0
        for shot in self.player.shots_group:
            shot.speed = 0

        if self.boss_spawned:
            self.boss.vert_speed = 0

        self.scroll_speed = 0
        self.player.speed = 0

    def unpause(self):
        for enemy in self.enemy_sprites:
            enemy.speed = enemy.original_speed
            for shot in enemy.shots_group:
                shot.speed = OBJECT_SPEEDS['shot']
        for shot in self.player.shots_group:
            shot.speed = OBJECT_SPEEDS['shot']

        if self.boss_spawned:
            self.boss.vert_speed = OBJECT_SPEEDS['boss']

        self.scroll_speed = OBJECT_SPEEDS['scroll']
        self.player.speed = OBJECT_SPEEDS['player']

    def update(self, dt):
        if self.showing_level_message:
            self.between_levels()
        else:
            self.update_bg_offset(dt)
            self.scroll(dt)
            self.spawn_enemy()
            self.all_sprites.draw(self.screen)
            self.all_sprites.update(dt)
            self.set_levels()
            self.game_win_or_game_over()
            self.dashboard.update(self.level_index)
        print(self.scroll_count)
