import os
import pygame


class Dashboard:
    """All dashboard text and calculations"""
    def __init__(self, screen, config_colors):
        super().__init__()

        self.screen = screen
        self.color = config_colors

        self.planet_dir = "assets/img/ui/rotating_planet_small"
        self.planet_frames = []
        self.planet_index = 0
        for planet_image in os.listdir(self.planet_dir):
            if planet_image.endswith(".png"):
                planet_filename = os.path.join(self.planet_dir, planet_image)
                planet_frame = pygame.image.load(planet_filename).convert_alpha()
                self.planet_frames.append(planet_frame)

        self.font = pygame.font.Font("assets/font/visitor1.ttf", 10)
        self.life_img = pygame.image.load("assets/img/ui/ship_8x8.png").convert_alpha()

        self.headers = ["SCORE", "LIVES", "ENERGY"]
        self.headers_x_pos = 288
        self.headers_y_pos = [50, 80, 115, 160]

        self.score = 0
        self.lives = 3

    def draw_dashboard_bg(self):
        pygame.draw.rect(self.screen, self.color["GREY"], pygame.Rect(256, 0, 64, 180))

    def draw_logo(self):
        self.planet_index += 0.1
        if self.planet_index >= len(self.planet_frames):
            self.planet_index = 0
        image = self.planet_frames[int(self.planet_index)]
        rect = image.get_rect(midtop=(self.headers_x_pos, 6))
        self.screen.blit(image, rect)

    def draw_headers(self):
        text_list = [self.font.render(header, False, self.color["WHITE"]) for header in self.headers]

        for i, text in enumerate(text_list):
            rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[i]))
            self.screen.blit(text, rect)

    def draw_score(self):
        text = self.font.render("{:06}".format(self.score), False, self.color["WHITE"])
        rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[0] + 10))
        self.screen.blit(text, rect)

    def draw_lives(self, lives):
        life_x = self.headers_x_pos - 16
        life_y = self.headers_y_pos[1] + 12

        for _ in range(0, lives-1):
            self.screen.blit(self.life_img, (life_x, life_y))
            life_x += 12

    def draw_energy(self, current_energy, max_energy):
        energy_bar_length = 50
        ratio = max_energy / energy_bar_length
        bar_width = current_energy / ratio

        energy_bar = pygame.Rect(self.headers_x_pos-25, self.headers_y_pos[2]+14, bar_width, 8)
        energy_bar_outline = pygame.Rect(self.headers_x_pos-26, self.headers_y_pos[2]+13, energy_bar_length+2, 10)

        pygame.draw.rect(self.screen, self.color["RED"], energy_bar)
        pygame.draw.rect(self.screen, self.color["YELLOW"], energy_bar_outline, 1)

    def draw_levels(self, level):
        text = self.font.render("LEVEL {}".format(level), False, self.color["WHITE"])
        rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[3]))
        self.screen.blit(text, rect)

    def update(self, lives, energy, max_energy, level):
        self.draw_dashboard_bg()
        self.draw_logo()
        self.draw_headers()
        self.draw_score()
        self.draw_lives(lives)
        self.draw_energy(energy, max_energy)
        self.draw_levels(level)
