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

        self.bg_dir = "assets/img/ui/welcome_screen_bg"
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


class GameOverScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font("assets/font/visitor1.ttf", 10)

    def show(self):

        self.screen.fill("black")

        game_over_text = self.font.render("GAME OVER", True, "red")
        restart_text = self.font.render("Press 'R' TO RESTART", True, "white")

        game_over_rect = game_over_text.get_rect()
        restart_rect = restart_text.get_rect()

        game_over_rect.center = (self.screen_width // 2, self.screen_height // 2)
        restart_rect.center = (self.screen_width // 2, self.screen_height // 2 + 10)

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)


class CongratsScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font("assets/font/visitor1.ttf", 10)

        self.astronaut_img = pygame.image.load("assets/img/ui/astronaut.png").convert_alpha()
        self.astronaut_img_rect = self.astronaut_img.get_rect(center=(400, 50))

    def show(self):

        self.screen.fill("black")

        self.screen.blit(self.astronaut_img, self.astronaut_img_rect)
        self.astronaut_img_rect.x -= 1
        if self.astronaut_img_rect.right < 0:
            self.astronaut_img_rect.center = (400, 50)

        text1 = self.font.render("congratulations, space resistance saved the planet", True, "white")
        text2 = self.font.render("alien attack has stopped and people live happy lives", True, "white")
        restart_text = self.font.render("press 'r' to restart game", True, "white")

        text1_rect = text1.get_rect()
        text2_rect = text2.get_rect()
        restart_rect = restart_text.get_rect()

        text1_rect.center = (self.screen_width // 2, self.screen_height // 2 - 10)
        text2_rect.center = (self.screen_width // 2, self.screen_height // 2)
        restart_rect.center = (self.screen_width // 2, self.screen_height // 2 + 30)

        self.screen.blit(text1, text1_rect)
        self.screen.blit(text2, text2_rect)
        self.screen.blit(restart_text, restart_rect)
