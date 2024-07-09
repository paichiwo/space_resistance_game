from src.config import *
from src.timer import Timer
from src.helpers import import_image, import_assets
from src.high_score_manager import HighScoreManager


class WelcomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.mid_screen = (WIDTH // 2, HEIGHT // 2)

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

    def welcome_scene(self):
        self.draw_planet()
        self.draw_logo()

        for text, color, offset in WELCOME_SCREEN_MESSAGES:
            self.draw_text(text, (self.mid_screen[0], self.mid_screen[1] + offset), FONT10, color)

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

    def update(self):
        self.draw_background()
        self.animation_timer.update()
        self.scene_switch_timer.update()

        if self.show_welcome_scene:
            self.welcome_scene()
        else:
            self.high_score_scene()
        self.draw_version()
