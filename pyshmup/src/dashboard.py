import pygame


class Dashboard:
    """All dashboard text and calculations"""
    def __init__(self, screen):
        super().__init__()

        self.screen = screen

        self.font = pygame.font.Font("assets/font/visitor1.ttf", 10)
        self.logo_img = pygame.image.load("assets/img/ui/pyshmup_logo.png").convert_alpha()
        self.life_img = pygame.image.load("assets/img/ui/ship_8x8.png").convert_alpha()
        self.rect = self.logo_img.get_rect(midtop=(288, 12))

        self.headers = ["SCORE", "LIVES", "ENERGY"]
        self.headers_x_pos = 288
        self.headers_y_pos = [50, 85, 120]

        self.score = 0
        self.lives = 3

    def draw_dashboard_bg(self):
        pygame.draw.rect(self.screen, "grey2", pygame.Rect(256, 0, 64, 180))

    def draw_logo(self):
        self.screen.blit(self.logo_img, self.rect)

    def draw_headers(self):
        text_list = [self.font.render(header, False, "white") for header in self.headers]
        for i, text in enumerate(text_list):
            rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[i]))
            self.screen.blit(text, rect)

    def draw_score(self):
        text = self.font.render("{:06}".format(self.score), False, "white")
        rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[0] + 10))
        self.screen.blit(text, rect)

    def draw_lives(self):
        pass

    def draw_energy(self, current_energy, max_energy):
        energy_bar_length = 50
        ratio = max_energy / energy_bar_length
        bar_width = current_energy / ratio
        x = pygame.draw.rect(self.screen, "red", pygame.Rect(self.headers_x_pos-25, self.headers_y_pos[2]+14, bar_width, 8))

    def update(self, energy, max_energy):
        self.draw_dashboard_bg()
        self.draw_logo()
        self.draw_headers()
        self.draw_score()
        self.draw_energy(energy, max_energy)
