import os

import pygame


class WelcomeScreen:
    def __init__(self, screen, screen_width, screen_height, colors):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors
        self.mid_screen = (self.screen_width // 2, self.screen_height // 2)
        self.font = pygame.font.Font("assets/font/visitor1.ttf", 10)

        self.bg_dir = "assets/img/ui/welcome_screen"
        self.bg_frames = []
        self.bg_index = 0
        for bg_image in os.listdir(self.bg_dir):
            if bg_image.endswith(".png"):
                bg_filename = os.path.join(self.bg_dir, bg_image)
                bg_frame = pygame.image.load(bg_filename).convert_alpha()
                self.bg_frames.append(bg_frame)

        self.planet_dir = "assets/img/ui/rotating_planet"
        self.planet_frames = []
        self.planet_index = 0
        for planet_image in os.listdir(self.planet_dir):
            if planet_image.endswith(".png"):
                planet_filename = os.path.join(self.planet_dir, planet_image)
                planet_frame = pygame.image.load(planet_filename).convert_alpha()
                self.planet_frames.append(planet_frame)

        self.planet_glow = pygame.image.load("assets/img/ui/rotating_planet/glow/glow.png")
        self.logo = pygame.image.load("assets/img/ui/space_resistance_logo.png").convert_alpha()

        self.anim_delay = 100
        self.bg_last_anim_update = pygame.time.get_ticks()
        self.planet_last_anim_update = pygame.time.get_ticks()

    def show(self):

        self.screen.fill("black")

        # Background animation
        cur = pygame.time.get_ticks()
        if cur - self.bg_last_anim_update >= self.anim_delay:
            self.bg_index = (self.bg_index + 1) % len(self.bg_frames)
            self.bg_last_anim_update = cur

        bg_frame = self.bg_frames[self.bg_index]
        self.screen.blit(bg_frame, (0, 0))

        # Planet animation
        cur = pygame.time.get_ticks()
        if cur - self.planet_last_anim_update >= self.anim_delay:
            self.planet_index = (self.planet_index + 1) % len(self.planet_frames)
            self.planet_last_anim_update = cur

        glow_rect = self.planet_glow.get_rect(center=(self.mid_screen[0], self.mid_screen[1] - 20))
        self.screen.blit(self.planet_glow, glow_rect)

        planet_frame = self.planet_frames[self.planet_index]
        planet_rect = planet_frame.get_rect(center=(self.mid_screen[0], self.mid_screen[1] - 20))
        self.screen.blit(planet_frame, planet_rect)

        # Logo display
        logo_rect = self.logo.get_rect(center=(self.mid_screen[0], self.mid_screen[1] - 20))
        self.screen.blit(self.logo, logo_rect)

        # Text 1
        message_text = self.font.render("MADE BY PAICHIWO USING PYTHON / PYGAME", True, self.colors["WHITE"])
        message_rect = message_text.get_rect(center=(self.mid_screen[0], self.mid_screen[1] + 60))
        self.screen.blit(message_text, message_rect)

        # Text 2
        start_text = self.font.render("PRESS 'S' TO START", True, self.colors["WHITE"])
        start_rect = start_text.get_rect(center=(self.mid_screen[0], self.mid_screen[1] + 70))
        self.screen.blit(start_text, start_rect)