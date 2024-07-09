import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.scenes import WelcomeScreen
from src.level_manager import LevelManager
from src.sound_manager import SoundManager


class Game:
    def __init__(self):
        self.enemy_kills = 0
        self.boss_killed = False
        self.first_level_msg = False

        self.states = {
            'welcome_screen_running': True,
            'game_running': False,
            'game_over_screen_running': False,
            'congrats_screen_running': False
        }

        # Game Setup
        self.clock = pygame.time.Clock()
        # Scaled Window
        self.window = pygame.Window(size=(WIDTH * SCALE, HEIGHT * SCALE), title=f'{TITLE} v{VERSION}')
        self.window.resizable = True
        self.renderer = sdl2.Renderer(self.window)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()

        # Sound Manager
        self.sound_manager = SoundManager()

        # Game Objects
        self.welcome_screen = WelcomeScreen(self.screen)
        self.level_manager = LevelManager(self.screen, self.renderer, self.sound_manager)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not self.states['game_running']:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.restart_game()

    def set_music_for_game(self):
        if self.states['welcome_screen_running']:
            self.sound_manager.play_music(MUSIC_TRACKS['welcome_screen_music'])
        elif (self.level_manager.level_index + 1 in [1, 2, 3]
              and not self.states['game_over_screen_running']
              and not self.states['congrats_screen_running']):
            self.sound_manager.play_music(MUSIC_TRACKS['levels_1_3_music'])

    def reset_game_values(self):
        pass

    def restart_game(self):
        self.reset_game_values()
        self.states['welcome_screen_running'] = False
        self.states['game_running'] = True
        self.level_manager.restart()
        self.welcome_screen.retrieve_scores()

    def game_over(self, game_over):
        if game_over:
            self.states['game_running'] = False
            self.states['welcome_screen_running'] = True
            self.welcome_screen.reset()

    def run(self):
        while True:
            self.set_music_for_game()
            # self.screen.fill(COLORS['BLACK'])
            self.renderer.clear()

            for event in pygame.event.get():
                self.handle_game_events(event)

            dt = self.clock.tick() / 1000
            if self.states['welcome_screen_running']:
                self.welcome_screen.update()
            else:
                if self.states['game_running']:
                    self.level_manager.update(dt)
                    self.game_over(self.level_manager.player.game_over)

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()


if __name__ == '__main__':
    Game().run()
