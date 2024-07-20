from src.config import *
from src.helpers import import_image


class Dashboard:
    def __init__(self, screen, player):
        super().__init__()
        self.screen = screen
        self.player = player

        self.life_img = import_image('assets/img/ui/life/0.png')

    def draw_energy(self):
        bar_length = 50
        ratio = self.player.max_energy / bar_length
        bar_width = self.player.current_energy / ratio

        pygame.draw.rect(self.screen, COLORS['RED'], pygame.Rect(10, 7, bar_width, 1))
        pygame.draw.rect(self.screen, 'indigo', pygame.Rect(9, 6, bar_length + 2, 3), 1)

    def draw_lives(self):
        x = 86
        for _ in range(0, self.player.lives-1):
            self.screen.blit(self.life_img, (x, 3))
            x += 12

    def draw_score(self):
        text = FONT10.render('{:07}'.format(self.player.score), False, COLORS['WHITE'])
        rect = text.get_rect(topleft=(143, 2))
        self.screen.blit(text, rect)

    def draw_levels(self, level):
        text = FONT10.render('LEVEL {}'.format(level + 1), False, COLORS['WHITE'])
        rect = text.get_rect(topleft=(209, 2))
        self.screen.blit(text, rect)

    def update(self, level):
        self.draw_score()
        self.draw_lives()
        self.draw_energy()
        self.draw_levels(level)
