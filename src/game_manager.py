import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.scenes import WelcomeScreen, GameOverScreen, CongratsScreen
from src.level_manager import LevelManager
from src.sound_manager import SoundManager
from src.high_score_manager import HighScoreManager

# redesign: welcome screen - implement menu - start, options, credits
# add: the lowest score to beat to the dashboard
# implement: new enemy following paths logic
# implement: first level message


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

        # User Name
        self.user_name = ''

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
        if event.type == pygame.KEYDOWN:
            if self.states['welcome_screen_running'] and event.key == pygame.K_s:
                self.restart_game()

            if self.states['congrats_screen_running']:
                if event.key == pygame.K_BACKSPACE:
                    self.user_name = self.user_name[:-1]
                elif len(self.user_name) < 8 and event.key != pygame.K_RETURN:
                    self.user_name += event.unicode if event.unicode in ALLOWED_CHARACTERS else ''
                if event.key == pygame.K_RETURN:
                    if len(self.user_name) >= 1:
                        self.states['score_entered'] = True

        # Full screen
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            self.window.set_fullscreen(True)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.window.set_windowed()

    def set_music_for_game(self):
        if self.states['welcome_screen_running']:
            self.sound_manager.play_music(MUSIC_TRACKS['welcome_screen_music'])
        elif self.states['game_over_screen_running']:
            self.sound_manager.play_music(MUSIC_TRACKS['game_over_screen'])
        elif self.states['congrats_screen_running']:
            self.sound_manager.play_music(MUSIC_TRACKS['congrats_screen'])
        elif self.states['game_running']:
            if self.level_manager.level_index in [0, 1, 2]:
                self.sound_manager.play_music(MUSIC_TRACKS['levels_1_3_music'])
            elif self.level_manager.level_index == 3:
                self.sound_manager.play_music(MUSIC_TRACKS['level_4'])

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

    def check_high_score(self):
        high_score = self.high_score_manager.check_high_score(self.level_manager.player.score)
        if high_score:
            self.congrats_screen.high_score_entry(self.user_name)
        else:
            self.user_name = ''
            self.congrats_screen.not_high_score()

        if self.states['score_entered']:
            self.high_score_manager.save_score(self.user_name, self.level_manager.player.score)
            self.welcome_screen.reset()
            self.states['congrats_screen_running'] = False
            self.states['welcome_screen_running'] = True

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
                self.game_over_screen.update()

            if self.states['congrats_screen_running']:
                self.congrats_screen.update(dt)
                self.check_high_score()

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()
