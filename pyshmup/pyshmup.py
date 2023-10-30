import pygame
import pygame._sdl2 as pg_sdl2
import random
import sys
from src.utils import Config
from src.player import Player, Fumes
from src.background import Background
from src.enemy import Enemy
from src.explosion import Explosion
from src.dashboard import Dashboard
from src.welcome_screen import WelcomeScreen
from src.game_over_screen import GameOverScreen
from src.powerup import PowerUp


class Game:

    def __init__(self):

        # Load config
        self.c = Config()
        self.config_colors = self.c.color()
        self.enemy_choice_for_level = self.c.enemy_choices()
        self.enemy_speeds = self.c.enemy_speed()
        self.enemy_spawning_intervals = self.c.enemy_spawning_times()

        # Game constants
        self.window_width = 320
        self.window_height = 180
        self.scale = 4
        self.fps = 120
        self.running = True
        self.level = 1
        self.enemy_kills = 0

        # Game setup
        pygame.init()
        pygame.display.set_caption("pyshump")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height),
                                              flags=pygame.RESIZABLE | pygame.HIDDEN | pygame.SCALED,
                                              vsync=1)
        self.clock = pygame.time.Clock()

        # Scaled window setup
        self.window = pg_sdl2.Window.from_display_module()
        self.window.size = (self.window_width * self.scale, self.window_height * self.scale)
        self.window.position = pg_sdl2.WINDOWPOS_CENTERED
        self.window.show()

        # Create game objects
        self.welcome_screen = WelcomeScreen(self.screen, self.window_width, self.window_height, self.config_colors)
        self.game_over_screen = GameOverScreen(self.screen, self.window_width, self.window_height)
        self.dashboard = Dashboard(self.screen, self.config_colors)
        self.bg = Background(self.screen, self.window_height)
        self.player = Player(self.bg.bg_1.get_width(), self.window_height)
        self.fumes = Fumes()

        # Create game sprites
        self.player_sprite = pygame.sprite.Group(self.fumes, self.player)
        self.enemy_sprite_group = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        # Timers
        self.enemy_timer_1 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_timer_1, 1500)

        self.energy_powerup_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.energy_powerup_timer, 5000)

        # God mode when life lost
        self.last_collision_time = 0
        self.god_mode = False
        self.god_timer = None

        # Life lost message
        self.font10 = pygame.font.Font("assets/font/visitor1.ttf", 10)
        self.font = pygame.font.Font("assets/font/visitor1.ttf", 20)
        self.life_lost_text = None
        self.life_lost_outline = None
        self.life_lost_timer = 0

        # Start game with welcome screen
        self.welcome_screen_active = True
        self.first_level_message = False

    def handle_events(self, event):
        """Handle game events"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if self.welcome_screen_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.welcome_screen_active = False
        else:
            if self.running:
                if event.type == self.enemy_timer_1:
                    self.set_timers_for_level()
                    self.set_enemies_for_level()
                if event.type == self.energy_powerup_timer:
                    self.powerups.add(PowerUp("energy", self.bg.bg.get_width(), self.window_height))
                    pygame.time.set_timer(self.energy_powerup_timer, 15000)
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.running = True

    def update_game(self):
        """Update all game objects"""
        self.screen.fill("black")

        self.bg.update()

        # Draw game elements
        self.player_sprite.draw(self.screen)
        self.player.shots.draw(self.screen)
        self.enemy_sprite_group.draw(self.screen)
        self.explosions.draw(self.screen)
        self.powerups.draw(self.screen)

        # Update game elements
        self.player.update(self.god_mode)
        self.fumes.update((self.player.rect.midbottom[0], self.player.rect.midbottom[1] + 8))
        self.enemy_sprite_group.update()
        self.explosions.update()
        self.powerups.update()
        self.dashboard.update(self.player.lives, self.player.cur_energy, self.player.max_energy, self.level)

        # Check collisions
        self.player_shot_collision()
        self.player_enemy_collision()
        self.enemy_shot_collision()
        self.powerup_collision()
        self.check_god_mode()

        # Show messages
        self.show_lost_life_msg()

        # Change levels
        self.change_level()

    def set_timers_for_level(self):
        if self.level in self.enemy_spawning_intervals:
            min_interval, max_interval = self.enemy_spawning_intervals[self.level]
            pygame.time.set_timer(self.enemy_timer_1, random.randint(min_interval, max_interval))

    def set_enemies_for_level(self):
        level = str(self.level)
        if level in self.enemy_choice_for_level:
            width = self.bg.bg.get_width()
            height = self.window_height
            choices = [entry["choice"] for entry in self.enemy_choice_for_level[level]]
            probabilities = [entry["probability"] for entry in self.enemy_choice_for_level[level]]
            enemy_choice = random.choices(choices, probabilities)[0]
            enemy_speeds = self.set_enemy_speeds()
            self.enemy_sprite_group.add(Enemy(self.screen, width, height, enemy_choice, self.player.rect, enemy_speeds))

    def set_enemy_speeds(self):
        level = str(self.level)
        if level in self.enemy_speeds:
            speeds = self.enemy_speeds[level]
            return speeds

    def change_level(self):
        if self.bg.scroll_count == 1:
            self.level += 1
            self.bg.change_bg(self.level)
            self.show_level_message()
            self.reset_level_values()

    def show_level_message(self):
        start = pygame.time.get_ticks()
        level_text = self.font.render(f"Level {self.level}", False, self.config_colors["WHITE"])
        level_rect = level_text.get_rect(midtop=(self.window_width // 2, self.window_height // 2))
        kills_text = self.font10.render(f"Enemy Kills: {self.enemy_kills}", False, self.config_colors["WHITE"])
        kills_rect = kills_text.get_rect(midtop=(self.window_width // 2, self.window_height // 2 + 30))

        while pygame.time.get_ticks() - start < 2000:
            self.screen.fill(self.config_colors["BLACK"])
            self.screen.blit(level_text, level_rect)
            self.screen.blit(kills_text, kills_rect)
            pygame.display.flip()

    def show_first_level_message(self):
        if not self.first_level_message:
            start_time = pygame.time.get_ticks()
            text = self.font.render(f"Level {self.level}", False, self.config_colors["WHITE"])
            rect = text.get_rect(midtop=(self.window_width // 2, self.window_height // 2))
            while pygame.time.get_ticks() - start_time < 2000:
                self.screen.fill(self.config_colors["BLACK"])
                self.screen.blit(text, rect)
                pygame.display.flip()
            self.screen.fill(self.config_colors["BLACK"])
            pygame.display.flip()
            self.first_level_message = True

    def player_shot_collision(self):
        """When shot collides with the Enemy"""
        for shot in self.player.shots:
            hits = pygame.sprite.spritecollide(shot, self.enemy_sprite_group, False)
            if hits:
                shot.kill()
                for hit_enemy in hits:
                    hit_enemy.deduct_energy(self.player.shot_power)
                    self.dashboard.score += hit_enemy.shot_score
                    self.explosions.add(Explosion(hit_enemy.rect.center))
                for enemy in self.enemy_sprite_group:
                    if enemy.energy <= 0:
                        enemy.kill()
                        self.explosions.add(Explosion(enemy.rect.center))
                        self.dashboard.score += enemy.kill_score
                        self.enemy_kills += 1

    def player_enemy_collision(self):
        collision_detected = False
        cur_time = pygame.time.get_ticks()

        for enemy in self.enemy_sprite_group:
            if (cur_time - self.last_collision_time >= 500
                    and pygame.sprite.collide_mask(self.player, enemy)
                    and not collision_detected
                    and not self.god_mode):
                self.player.get_damage(enemy.bump_power)
                self.explosions.add(Explosion(self.player.rect.center))
                self.last_collision_time = pygame.time.get_ticks()
                self.deduct_life()

    def enemy_shot_collision(self):
        """When shot collides with the Enemy"""
        for sprite in self.enemy_sprite_group.sprites():
            for shot in sprite.shots:
                hits = pygame.sprite.collide_mask(shot, self.player)
                if hits:
                    shot.kill()
                    self.player.cur_energy -= sprite.shot_power
                    self.explosions.add(Explosion(shot.rect.center))
                    self.deduct_life()

    def powerup_collision(self):
        for powerup in self.powerups:
            if pygame.sprite.collide_mask(powerup, self.player):
                self.player.cur_energy = powerup.action(self.player.cur_energy, self.player.max_energy)
                powerup.kill()

    def deduct_life(self):
        if self.player.cur_energy <= 0:
            self.player.cur_energy = self.player.max_energy
            if self.player.lives > 0:
                self.player.lives -= 1

                # set invincibility
                self.god_mode = True
                self.god_timer = pygame.time.get_ticks() + 4000

                # stop spawning enemies for 2s
                self.enemy_sprite_group.empty()
                pygame.time.set_timer(self.enemy_timer_1, 2000)

                # set data for a life-lost message
                self.life_lost_outline = self.font.render("LIFE LOST", False, self.config_colors["BLACK"])
                self.life_lost_text = self.font.render("LIFE LOST", False, self.config_colors["WHITE"])
                self.life_lost_timer = self.god_timer - 500  # message display time

    def check_god_mode(self):
        if self.god_mode and pygame.time.get_ticks() >= self.god_timer:
            self.god_mode = False

    def show_lost_life_msg(self):
        if self.life_lost_text and pygame.time.get_ticks() <= self.life_lost_timer:
            self.screen.blit(self.life_lost_outline, (self.bg.bg_1.get_width() // 2 - 54, self.window_height // 2 - 19))
            self.screen.blit(self.life_lost_text, (self.bg.bg_1.get_width() // 2 - 55, self.window_height // 2 - 20))

    def game_over(self):
        return self.player.lives > 0

    def reset_level_values(self):
        self.god_mode = False
        self.enemy_sprite_group.empty()
        self.powerups.empty()
        self.enemy_kills = 0
        pygame.time.set_timer(self.energy_powerup_timer, 5000)

    def reset_game_values(self):
        self.level = 1
        self.bg.bg = self.bg.level_images[0]
        self.dashboard.score = 0
        self.player.lives = 4
        self.player.cur_energy = 100
        self.god_mode = False
        self.enemy_sprite_group.empty()
        self.powerups.empty()
        self.enemy_kills = 0
        pygame.time.set_timer(self.enemy_timer_1, 2000)

    def game_loop(self):
        while True:
            for event in pygame.event.get():
                self.handle_events(event)
            if self.welcome_screen_active:
                self.welcome_screen.show()
            else:
                self.show_first_level_message()
                if self.running:
                    self.update_game()
                    self.running = self.game_over()
                else:
                    self.game_over_screen.show()
                    self.reset_game_values()

            pygame.display.update()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    Game().run()
