import math
from src.config import *
from src.timer import Timer
from src.helpers import import_image, import_assets
from src.high_score_manager import HighScoreManager
from src.main_menu import MainMenu


class WelcomeScreen:
    def __init__(self, screen, window, states, sound_manager, restart_game):
        self.screen = screen
        self.window = window
        self.states = states
        self.sound_manager = sound_manager
        self.restart_game = restart_game
        self.mid_screen = (WIDTH / 2, HEIGHT / 2)

        self.bg_frames = import_assets('assets/img/ui/welcome_screen_bg')
        self.planet_frames = import_assets('assets/img/ui/rotating_planet')
        self.planet_glow = import_image('assets/img/ui/rotating_planet/glow/glow.png')
        self.logo = import_image('assets/img/ui/logo/logo.png')
        self.bg_index = self.planet_index = 0

        self.animation_timer = Timer(100, self.update_animation_indices, repeat=True, autostart=True)
        self.scene_switch_timer = Timer(5000, self.switch_scene, repeat=True, autostart=True)
        self.show_welcome_scene = True

        self.high_score_manager = HighScoreManager()
        self.high_scores = None
        self.retrieve_scores()

        self.main_menu = MainMenu(self.screen, self.window, self.states, self.sound_manager, self.restart_game)

    def update_animation_indices(self):
        self.bg_index = (self.bg_index + 1) % len(self.bg_frames)

        self.planet_index += 1
        if self.planet_index >= len(self.planet_frames):
            self.planet_index = 0

    def draw_background(self):
        bg_frame = self.bg_frames[self.bg_index]
        self.screen.blit(bg_frame, (0, 0))

    def draw_planet(self):
        glow_rect = self.planet_glow.get_rect(center=(self.mid_screen[0], self.mid_screen[1] - 30))
        self.screen.blit(self.planet_glow, glow_rect)

        planet_frame = self.planet_frames[self.planet_index]
        planet_rect = planet_frame.get_rect(center=(self.mid_screen[0], self.mid_screen[1] - 30))
        self.screen.blit(planet_frame, planet_rect)

    def draw_logo(self):
        logo_rect = self.logo.get_rect(center=(self.mid_screen[0], self.mid_screen[1] - 30))
        self.screen.blit(self.logo, logo_rect)

    def draw_text(self, text, position, font, color):
        message_text = font.render(text, True, color)
        message_rect = message_text.get_rect(center=position)
        self.screen.blit(message_text, message_rect)

    def draw_version(self):
        self.draw_text(f'v{VERSION}', (WIDTH - 12, 6), FONT10, COLORS['WHITE'])

    def welcome_scene(self, event):
        self.draw_planet()
        self.draw_logo()
        self.main_menu.update(event)

    def high_score_scene(self):
        self.draw_text('HIGH SCORES:', (self.mid_screen[0], self.mid_screen[1] - 60), FONT20, COLORS['WHITE'])

        y_pos = 0
        for score in self.high_scores:
            self.draw_text(f'{score[0]}: {score[1]}', (self.mid_screen[0], self.mid_screen[1] - 40 + y_pos), FONT10,
                           COLORS['WHITE'])
            y_pos += 10

    def switch_scene(self):
        self.show_welcome_scene = not self.show_welcome_scene

    def retrieve_scores(self):
        self.high_scores = self.high_score_manager.retrieve_all_scores()

    def reset(self):
        self.retrieve_scores()
        self.scene_switch_timer = Timer(5000, self.switch_scene, repeat=True, autostart=True)

    def update(self, event):
        self.draw_background()
        self.animation_timer.update()
        self.scene_switch_timer.update()
        self.draw_version()

        if self.show_welcome_scene:
            self.welcome_scene(event)
        else:
            self.high_score_scene()


class GameOverScreen:
    def __init__(self, screen):
        self.screen = screen

    def draw_text(self):
        texts = [FONT10.render('GAME OVER', True, COLORS['RED']),
                 FONT10.render('PRESS "R" TO RESTART', True, COLORS['WHITE']), ]

        x_pos = WIDTH / 2
        y_pos = HEIGHT / 2

        for text in texts:
            self.screen.blit(text, text.get_rect(center=(x_pos, y_pos)))
            y_pos += 10

    def update(self):
        self.draw_text()


class CongratsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.frames = import_assets('assets/img/ui/astronaut/')
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_frect(center=(300, 40))
        self.time_elapsed = 0  # To track the elapsed time for the scaling effect

    def animate_astronaut(self, dt):
        self.index = (self.index + 10 * dt) % len(self.frames)
        self.image = self.frames[int(self.index)]

    def move_astronaut(self, dt):
        self.rect.x -= 30 * dt
        if self.rect.right <= -10:
            self.rect.center = (300, 40)
        self.screen.blit(self.image, self.rect)

    def draw_astronaut_text(self, dt):
        self.time_elapsed += dt
        scale_factor = 1 + math.sin(self.time_elapsed * .8 * math.pi)

        texts = [
            FONT10.render('YOU', True, COLORS['BLACK']),
            FONT10.render('WIN', True, COLORS['BLACK'])
        ]
        x_pos = [self.rect.x + 19, self.rect.x + 26]
        y_pos = [self.rect.y + 13, self.rect.y + 24]

        for text, x_position, y_position in zip(texts, x_pos, y_pos):
            text_rect = text.get_rect(center=(x_position, y_position))
            scaled_text = pygame.transform.scale(text,
                                                 (int(text_rect.width * scale_factor),
                                                  int(text_rect.height * scale_factor)))
            scaled_rect = scaled_text.get_rect(center=text_rect.center)
            self.screen.blit(scaled_text, scaled_rect.topleft)

    def high_score_entry(self, user_name):
        user_name_text = FONT20.render(user_name, True, COLORS['WHITE'])
        self.screen.blit(user_name_text, user_name_text.get_rect(center=(WIDTH / 2, HEIGHT / 2)))

        pygame.draw.rect(self.screen, 'indigo', ((WIDTH / 2 - 52, HEIGHT / 2 - 10), (102, 20)), 2)

        texts = [
            FONT10.render('CONGRATULATIONS, YOU BEAT THE HIGH SCORE', True, COLORS['YELLOW']),
            FONT10.render('PLEASE ENTER YOUR NAME', True, COLORS['YELLOW'])
        ]
        x_pos = WIDTH / 2
        y_pos = [120, 132]

        for text, y_position in zip(texts, y_pos):
            self.screen.blit(text, text.get_rect(center=(x_pos, y_position)))

    def not_high_score(self):
        texts = [
            FONT10.render('CONGRATULATIONS, YOU BEAT THE GAME', True, COLORS['YELLOW']),
            FONT10.render('YOUR SCORE IS TOO LOW FOR HIGH SCORES', True, COLORS['YELLOW'])
        ]
        x_pos = WIDTH / 2
        y_pos = [120, 132]

        for text, y_position in zip(texts, y_pos):
            self.screen.blit(text, text.get_rect(center=(x_pos, y_position)))

    def update(self, dt):
        self.animate_astronaut(dt)
        self.move_astronaut(dt)
        self.draw_astronaut_text(dt)
