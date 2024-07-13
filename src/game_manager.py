import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.scenes import WelcomeScreen, GameOverScreen, CongratsScreen
from src.level_manager import LevelManager
from src.sound_manager import SoundManager
from src.high_score_manager import HighScoreManager

# Redesign welcome screen - implement menu - start, options, credits
# add the lowest score to beat to the dashboard
# create entry in pygame and implement on congrats screen - player writes name inside pygame not
#      tkinter, and that name is saved to high_scores


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        # Scaled Window
        self.window = pygame.Window(size=(WIDTH * SCALE, HEIGHT * SCALE), title=f'{TITLE} v{VERSION}')
        self.window.resizable = True
        self.renderer = sdl2.Renderer(self.window)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()

        # States
        self.states = {
            'welcome_screen_running': True,
            'game_running': False,
            'game_over_screen_running': False,
            'congrats_screen_running': False,
            'score_entered': False
        }

        # Sound Manager
        self.sound_manager = SoundManager()

        # Hi Score Manager
        self.high_score_manager = HighScoreManager()

        # Game Objects
        self.welcome_screen = WelcomeScreen(self.screen)
        self.level_manager = LevelManager(self.screen, self.renderer, self.sound_manager)
        self.game_over_screen = GameOverScreen(self.screen)
        self.congrats_screen = CongratsScreen(self.screen)

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if self.states['welcome_screen_running']:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.restart_game()
        # Full screen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.window.set_fullscreen(True)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.window.set_windowed()

    def set_music_for_game(self):
        if self.states['welcome_screen_running']:
            self.sound_manager.play_music(MUSIC_TRACKS['welcome_screen_music'])
        elif (self.level_manager.level_index in [0, 1, 2]
              and not self.states['game_over_screen_running']
              and not self.states['congrats_screen_running']):
            self.sound_manager.play_music(MUSIC_TRACKS['levels_1_3_music'])

    def restart_game(self):
        self.states['welcome_screen_running'] = False
        self.states['game_running'] = True
        self.states['game_over_screen_running'] = False
        self.states['congrats_screen_running'] = False
        self.states['score_entered'] = False
        self.level_manager.restart()
        self.welcome_screen.reset()

    def game_over(self, game_over):
        if game_over:
            self.states['game_running'] = False
            self.states['game_over_screen_running'] = True
            self.welcome_screen.reset()

    def game_win(self, boss_killed):
        if boss_killed:
            self.states['game_running'] = False
            self.states['congrats_screen_running'] = True

    def high_score(self):
        if not self.states['score_entered']:
            self.high_score_manager.check_high_score(self.level_manager.player.score)
            self.states['score_entered'] = True

    def run(self):
        while True:
            self.set_music_for_game()
            self.screen.fill(COLORS['BLACK'])
            self.renderer.clear()

            for event in pygame.event.get():
                self.handle_game_events(event)

            dt = self.clock.tick() / 1000
            if self.states['welcome_screen_running']:
                self.welcome_screen.update()

            if self.states['game_running']:
                self.level_manager.update(dt)
                self.game_over(self.level_manager.game_over)
                self.game_win(self.level_manager.boss_killed)

            if self.states['game_over_screen_running']:
                self.game_over_screen.show()

            if self.states['congrats_screen_running']:
                self.congrats_screen.update(dt)
                self.high_score()

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()
