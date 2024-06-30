from src.config import *
from src.helpers import import_assets, import_image


class Dashboard:
    def __init__(self, screen, player):
        super().__init__()

        self.screen = screen
        self.player = player

        self.planet_frames = import_assets('assets/img/ui/rotating_planet_small')
        self.planet_index = 0
        self.life_img = import_image('assets/img/ui/life/0.png')

        self.headers_x_pos = 288
        self.headers_y_pos = [50, 80, 115, 160]

    def draw_dashboard_bg(self):
        pygame.draw.rect(self.screen, COLORS['GREY'], pygame.Rect(256, 0, 64, 180))

    def draw_logo(self, dt):
        self.planet_index += 18 * dt
        if self.planet_index >= len(self.planet_frames):
            self.planet_index = 0
        image = self.planet_frames[int(self.planet_index)]
        rect = image.get_rect(midtop=(self.headers_x_pos, 6))
        self.screen.blit(image, rect)

    def draw_headers(self):
        headers = ['SCORE', 'LIVES', 'ENERGY']
        text_list = [FONT10.render(header, False, COLORS['WHITE']) for header in headers]

        for i, text in enumerate(text_list):
            rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[i]))
            self.screen.blit(text, rect)

    def draw_score(self):
        text = FONT10.render('{:06}'.format(self.player.score), False, COLORS['WHITE'])
        rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[0] + 10))
        self.screen.blit(text, rect)

    def draw_lives(self):
        life_x = self.headers_x_pos - 16
        life_y = self.headers_y_pos[1] + 12

        for _ in range(0, self.player.lives-1):
            self.screen.blit(self.life_img, (life_x, life_y))
            life_x += 12

    def draw_energy(self):
        energy_bar_length = 50
        ratio = self.player.max_energy / energy_bar_length
        bar_width = self.player.current_energy / ratio

        energy_bar = pygame.Rect(self.headers_x_pos-25, self.headers_y_pos[2]+14, bar_width, 8)
        energy_bar_outline = pygame.Rect(self.headers_x_pos-26, self.headers_y_pos[2]+13, energy_bar_length+2, 10)

        pygame.draw.rect(self.screen, COLORS['RED'], energy_bar)
        pygame.draw.rect(self.screen, COLORS['YELLOW'], energy_bar_outline, 1)

    def draw_levels(self, level):
        text = FONT10.render('LEVEL {}'.format(level+1), False, COLORS['WHITE'])
        rect = text.get_rect(midtop=(self.headers_x_pos, self.headers_y_pos[3]))
        self.screen.blit(text, rect)

    def update(self, player, level, dt):
        self.draw_dashboard_bg()
        self.draw_logo(dt)
        self.draw_headers()
        self.draw_score()
        self.draw_lives()
        self.draw_energy()
        self.draw_levels(level)
