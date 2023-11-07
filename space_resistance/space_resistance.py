import pygame
import pygame._sdl2 as pg_sdl2
import random
import sys
from src.utils import Config
from src.player import Player, Fumes
from src.background import Background
from src.enemy import Enemy, Boss
from src.explosion import Explosion
from src.dashboard import Dashboard
from src.powerup import PowerUp
from src.game_screens import WelcomeScreen, GameOverScreen, CongratsScreen

# 1. delay after boss killed (display counting number of total enemies killed)
# 2. high-score system (implement saving scores on web)
# 3. music / sound effects(player_dead, explosion, player shot, level 1-3 music, level 4 music)


class Game:

    def __init__(self):

        # Load config
        self.level_msg = False
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

        # Game variables
        self.running = False
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
        self.congrats_screen = CongratsScreen(self.screen, self.window_width, self.window_height)
        self.dashboard = Dashboard(self.screen, self.config_colors)
        self.bg = Background(self.screen, self.window_height)
        self.player = Player(self.bg.bg.get_width(), self.window_height)
        self.fumes = Fumes()
        self.boss = Boss(self.screen, self.bg.bg.get_width(), self.window_height, self.player.rect)

        # Create game sprites
        self.player_sprite = pygame.sprite.Group(self.fumes, self.player)
        self.enemy_sprite_group = pygame.sprite.Group()
        self.boss_sprite = pygame.sprite.GroupSingle()
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

        # Game lost
        self.game_over_screen_active = False

        # Game won
        self.congrats_screen_active = False

        # Music
        # pygame.mixer.init(44100, 16, 4, 4096)
        # welcome screen
        self.welcome_screen_music = pygame.mixer.Sound("assets/msx/music/welcome_screen.wav")
        self.welcome_screen_music.set_volume(0.7)
        self.channel1 = pygame.mixer.Channel(1)
        # in game - levels 1-3
        self.levels_1_3_music = pygame.mixer.Sound("assets/msx/music/levels_1_to_3.wav")
        self.levels_1_3_music.set_volume(0.7)
        self.channel2 = pygame.mixer.Channel(2)
        # in game - level 4
        self.level_4_music = pygame.mixer.Sound("assets/msx/music/1min.wav")
        self.level_4_music.set_volume(0.7)
        self.channel3 = pygame.mixer.Channel(3)
        # # congrats screen
        self.congrats_screen_music = pygame.mixer.Sound("assets/msx/music/congrats.wav")
        self.congrats_screen_music.set_volume(0.7)
        self.channel4 = pygame.mixer.Channel(4)

        # Sound fx

    def handle_events(self, event):
        """Handle game events"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if self.welcome_screen_active:
            self.reset_game_values()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.game_over_screen_active = False
                self.welcome_screen_active = False
                self.congrats_screen_active = False
                self.running = True

        if self.game_over_screen_active:
            self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.welcome_screen_active = True

        if self.congrats_screen_active:
            self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.welcome_screen_active = True

        if self.level_msg:
            self.running = False

        else:
            if self.running:
                if event.type == self.enemy_timer_1:
                    self.set_timers_for_level()
                    self.set_enemies_for_level()
                if event.type == self.energy_powerup_timer:
                    self.powerups.add(PowerUp("energy", self.bg.bg.get_width(), self.window_height))
                    pygame.time.set_timer(self.energy_powerup_timer, 15000)
            else:
                # self.game_over_screen_active = True
                # self.show_game_over_screen()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.welcome_screen_active = True

    def show_game_over_screen(self):
        if self.game_over_screen_active:
            self.running = False
            self.game_over_screen.show()

    def update_game(self):
        """Update all game objects"""

        if not self.running:
            return

        self.screen.fill("black")

        # Change levels
        self.change_level()
        self.bg.update()
        self.set_last_level()

        # Draw game elements
        self.player_sprite.draw(self.screen)
        self.player.shots.draw(self.screen)
        self.enemy_sprite_group.draw(self.screen)
        self.boss_sprite.draw(self.screen)
        self.explosions.draw(self.screen)
        self.powerups.draw(self.screen)

        # Update game elements
        self.player.update(self.god_mode)
        self.fumes.update((self.player.rect.midbottom[0], self.player.rect.midbottom[1] + 8))
        self.enemy_sprite_group.update()
        self.boss_sprite.update()
        self.explosions.update()
        self.powerups.update()
        self.dashboard.update(self.player.lives, self.player.cur_energy, self.player.max_energy, self.level)

        # Check collisions
        self.player_shot_collision()
        self.player_enemy_collision()
        self.player_boss_collision()
        self.enemy_shot_collision()
        self.boss_shot_collision()
        self.powerup_collision()
        self.check_god_mode()

        # Show messages
        self.show_lost_life_msg()

        # Check if boss is killed
        self.is_boss_killed()

    def set_music_for_level_1_to_3(self):
        if self.welcome_screen_active:
            self.channel2.stop()
            self.channel3.stop()
            self.channel4.stop()
            if not self.channel1.get_busy():
                self.channel1.play(self.welcome_screen_music, loops=-1)
        elif self.level in [1, 2, 3]:
            self.channel1.stop()
            self.channel3.stop()
            self.channel4.stop()
            if not self.channel2.get_busy():
                self.channel2.play(self.levels_1_3_music, loops=-1)
        elif self.level == 4:
            self.channel1.stop()
            self.channel2.stop()
            self.channel4.stop()
            if not self.channel3.get_busy():
                self.channel3.play(self.level_4_music, loops=-1)
        elif self.congrats_screen_active and self.level == 4:
            self.channel1.stop()
            self.channel2.stop()
            self.channel3.stop()
            if not self.channel4.get_busy():
                self.channel4.play(self.congrats_screen_music, loops=-1)
        # else:
        #     self.channel1.stop()
        #     self.channel2.stop()
        #     self.channel3.stop()
        #     self.channel4.stop()

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

    def set_last_level(self):
        if self.level == 4:
            self.boss_sprite.add(self.boss)

    def set_enemy_speeds(self):
        level = str(self.level)
        if level in self.enemy_speeds:
            speeds = self.enemy_speeds[level]
            return speeds

    def change_level(self):
        if self.bg.scroll_count == 1 and not self.level == 4:
            self.level += 1
            self.bg.change_bg(self.level)
            self.show_level_message()

    def show_level_message(self):
        start = pygame.time.get_ticks()
        level_text = self.font.render(f"Level {self.level}", False, self.config_colors["WHITE"])
        level_rect = level_text.get_rect(midtop=(self.window_width // 2, self.window_height // 2))
        kills_text = self.font10.render(f"Enemy Kills: {self.enemy_kills}", False, self.config_colors["WHITE"])
        kills_rect = kills_text.get_rect(midtop=(self.window_width // 2, self.window_height // 2 + 30))

        while pygame.time.get_ticks() - start < 3000:
            self.level_msg = True
            self.screen.fill(self.config_colors["BLACK"])
            self.screen.blit(level_text, level_rect)
            self.screen.blit(kills_text, kills_rect)
            pygame.display.flip()
            self.reset_level_values()
        self.level_msg = False

    def show_first_level_message(self):
        if not self.first_level_message:
            self.first_level_message = True
            self.level_msg = True
            start_time = pygame.time.get_ticks()
            text = self.font.render(f"Level {self.level}", False, self.config_colors["WHITE"])
            rect = text.get_rect(midtop=(self.window_width // 2, self.window_height // 2))

            while pygame.time.get_ticks() - start_time < 2000:
                self.screen.fill(self.config_colors["BLACK"])
                self.screen.blit(text, rect)
                pygame.display.flip()
                self.reset_game_values()
            self.screen.fill(self.config_colors["BLACK"])
            pygame.display.flip()
            self.level_msg = False

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
                        self.explosions.add(Explosion(enemy.rect.center))
                        self.dashboard.score += enemy.kill_score
                        self.enemy_kills += 1
            boss_hits = pygame.sprite.spritecollide(shot, self.boss_sprite, False)
            if boss_hits:
                shot.kill()
                for hit_boss in boss_hits:
                    hit_boss.deduct_energy(self.player.shot_power)
                    print(self.boss.energy)
                    self.dashboard.score += hit_boss.shot_score
                    self.explosions.add(Explosion(hit_boss.rect.center))
                for boss in self.boss_sprite:
                    if boss.energy <= 0:
                        self.explosions.add(Explosion(boss.rect.center))
                        self.dashboard.score += boss.kill_score
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
        for sprite in self.enemy_sprite_group.sprites():
            for shot in sprite.shots:
                hits = pygame.sprite.collide_mask(shot, self.player)
                if hits:
                    shot.kill()
                    self.player.cur_energy -= sprite.shot_power
                    self.explosions.add(Explosion(shot.rect.center))
                    self.deduct_life()

    def player_boss_collision(self):
        collision_detected = False
        cur_time = pygame.time.get_ticks()
        for boss in self.boss_sprite:
            if (cur_time - self.last_collision_time >= 500
                    and pygame.sprite.collide_mask(self.player, boss)
                    and not collision_detected
                    and not self.god_mode):
                self.player.get_damage(boss.bump_power)
                self.explosions.add(Explosion(self.player.rect.center))
                self.last_collision_time = pygame.time.get_ticks()
                self.deduct_life()

    def boss_shot_collision(self):
        for sprite in self.boss_sprite.sprites():
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

    def is_boss_killed(self):
        if self.level == 4:
            if not self.boss_sprite:  # Check if the boss sprite is empty
                self.congrats_screen_active = True
                self.show_congrats_screen()
                self.boss_sprite.add(Enemy(self.screen, self.bg.bg.get_width(), self.window_height,
                                           "sm1", self.player.rect, self.set_enemy_speeds()))

    def show_congrats_screen(self):
        if self.congrats_screen_active:
            self.running = False
            self.congrats_screen.show()

    def game_over(self):
        return self.player.lives > 0

    def reset_level_values(self):
        self.god_mode = False
        self.enemy_sprite_group.empty()
        self.powerups.empty()
        self.enemy_kills = 0
        self.god_mode = False
        pygame.time.set_timer(self.enemy_timer_1, 2000)

    def reset_game_values(self):
        self.level = 1
        self.enemy_kills = 0
        self.player.lives = 4
        self.player.cur_energy = 100
        self.player.rect.midbottom = (self.bg.bg.get_width() // 2, self.window_height - 10)

        self.bg.bg = self.bg.level_images[0]
        self.dashboard.score = 0

        self.god_mode = False

        self.enemy_sprite_group.empty()
        self.powerups.empty()
        self.boss_sprite.empty()

        pygame.time.set_timer(self.enemy_timer_1, 2000)
        pygame.time.set_timer(self.energy_powerup_timer, 5000)

    def game_loop(self):
        while True:
            self.set_music_for_level_1_to_3()

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
                    if self.player.lives <= 0:
                        self.game_over_screen_active = True
                        self.show_game_over_screen()

            pygame.display.update()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    Game().run()