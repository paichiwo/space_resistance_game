import sys
import pygame._sdl2 as sdl2
from src.config import *
from src.scenes import WelcomeScreen, GameOverScreen, CongratsScreen
from src.level_manager import LevelManager
from src.sound_manager import SoundManager
from src.high_score_manager import HighScoreManager
from src.debug import DebugMenu

# redesign: welcome screen - implement menu - start, options, credits
# add: the lowest score to beat to the dashboard
# implement: new enemy following paths logic
# implement: first level message
# power-ups


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()

        # Scaled Window
        self.window = pygame.Window(size=(WIDTH * SCALE, HEIGHT * SCALE), title=f'{TITLE} v{VERSION}')
        self.window.resizable = True
        self.renderer = sdl2.Renderer(self.window, accelerated=True)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()

        self.window.position = (0, 30)
        self.fullscreen = False

        self.joysticks = {}

        # States
        self.states = {
            'welcome_screen_running': True,
            'game_running': False,
            'game_over_screen_running': False,
            'congrats_screen_running': False,
            'score_entered': False,
            'debug_visible': False
        }

        # User Name
        self.user_name = ''

        # Sound Manager
        self.sound_manager = SoundManager()

        # Hi Score Manager
        self.high_score_manager = HighScoreManager()

        # Game Objects
        self.welcome_screen = WelcomeScreen(self.screen, self.window, self.states, self.sound_manager, self.restart)
        self.level_manager = LevelManager(self.screen, self.renderer, self.sound_manager)
        self.game_over_screen = GameOverScreen(self.screen)
        self.congrats_screen = CongratsScreen(self.screen)

        # Debug
        self.debug_menu = DebugMenu(self.screen, self.level_manager, self.states)

    def add_joystick(self, device_index):
        joy = pygame.joystick.Joystick(device_index)
        self.joysticks[joy.get_instance_id()] = joy

    def remove_joystick(self, instance_id):
        if instance_id in self.joysticks:
            del self.joysticks[instance_id]

    def handle_game_events(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # joysticks
        elif event.type == pygame.JOYDEVICEADDED:
            self.add_joystick(event.device_index)
        elif event.type == pygame.JOYDEVICEREMOVED:
            self.remove_joystick(event.instance_id)

        # keyboard
        elif event.type == pygame.KEYDOWN:
            if self.states['congrats_screen_running']:
                if not self.welcome_screen.show_welcome_scene:
                    if event.key == pygame.K_BACKSPACE:
                        self.user_name = self.user_name[:-1]
                    elif len(self.user_name) < 8 and event.key != pygame.K_RETURN:
                        self.user_name += event.unicode if event.unicode in ALLOWED_CHARACTERS else ''
                    if event.key == pygame.K_RETURN:
                        if len(self.user_name) >= 1:
                            self.states['score_entered'] = True

            elif event.key == pygame.K_d:
                self.run_debug()

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

    def restart(self):
        self.states['welcome_screen_running'] = False
        self.states['game_running'] = True
        self.states['game_over_screen_running'] = False
        self.states['congrats_screen_running'] = False
        self.states['score_entered'] = False
        self.level_manager.restart()
        self.welcome_screen.reset()

    def check_game_win_or_game_over(self, game_over, boss_killed):
        if game_over:
            self.states['game_running'] = False
            self.states['game_over_screen_running'] = True
            self.welcome_screen.reset()
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

    def run_debug(self):
        self.states['debug_visible'] = not self.states['debug_visible']

    def run(self):
        event = None
        while True:
            self.screen.fill(COLORS['BLACK'])
            self.renderer.clear()
            self.set_music_for_game()

            for event in pygame.event.get():
                self.handle_game_events(event)

            dt = self.clock.tick() / 1000
            if self.states['welcome_screen_running']:
                self.welcome_screen.update(event)

            if self.states['game_running']:
                self.level_manager.update(dt)
                self.check_game_win_or_game_over(self.level_manager.game_over, self.level_manager.boss_killed)

            if self.states['game_over_screen_running']:
                self.game_over_screen.update()

            if self.states['congrats_screen_running']:
                self.congrats_screen.update(dt)
                self.check_high_score()

            if self.states['debug_visible']:
                self.debug_menu.update(event)
                self.level_manager.pause()
            else:
                self.level_manager.unpause()

            sdl2.Texture.from_surface(self.renderer, self.screen).draw()
            self.renderer.present()
