from src.config import *
from src.helpers import import_image


class Dashboard:
    def __init__(self, screen, player, lowest_score):
        super().__init__()
        self.screen = screen
        self.player = player
        self.lowest_score = lowest_score

        self.life_img = import_image('assets/img/ui/life/0.png')

    def draw_energy(self):
        bar_length = 30
        ratio = self.player.max_energy / bar_length
        bar_width = self.player.current_energy / ratio

        pygame.draw.rect(self.screen, COLORS['RED'], pygame.Rect(10, 7, bar_width, 1))
        pygame.draw.rect(self.screen, 'indigo', pygame.Rect(9, 6, bar_length + 2, 3), 1)

    def draw_lives(self):
        x = 47
        for _ in range(0, self.player.lives-1):
            self.screen.blit(self.life_img, (x, 3))
            x += 11

    def draw_score(self):
        bg_rect = pygame.rect.Rect(83, 3, 7, 7)

        icon_text = FONT10.render('S', True, COLORS['YELLOW'])
        icon_rect = icon_text.get_rect(topleft=(bg_rect.x + 1, bg_rect.y - 1))

        score_text = FONT10.render('{:07}'.format(self.player.score), True, COLORS['WHITE'])
        score_rect = score_text.get_rect(topleft=(bg_rect.x + 9, bg_rect.y - 1))

        pygame.draw.rect(self.screen, COLORS['INDIGO'], bg_rect)
        self.screen.blit(icon_text, icon_rect)
        self.screen.blit(score_text, score_rect)

    def draw_lowest_hi_score(self):
        bg_rect = pygame.rect.Rect(139, 3, 7, 7)

        icon_text = FONT10.render('H', True, COLORS['YELLOW'])
        icon_rect = icon_text.get_rect(topleft=(bg_rect.x + 1, bg_rect.y - 1))

        score_text = FONT10.render(f'{self.lowest_score:07}', True, COLORS['WHITE'])
        score_rect = score_text.get_rect(topleft=(bg_rect.x + 9, bg_rect.y - 1))

        pygame.draw.rect(self.screen, COLORS['INDIGO'], bg_rect)
        self.screen.blit(icon_text, icon_rect)
        self.screen.blit(score_text, score_rect)

    def draw_levels(self, level):
        bg_rect = pygame.rect.Rect(195, 3, 7, 7)

        icon_text = FONT10.render('L', True, COLORS['YELLOW'])
        icon_rect = icon_text.get_rect(topleft=(bg_rect.x + 1, bg_rect.y - 1))

        level_text = FONT10.render('{}'.format(level + 1), True, COLORS['WHITE'])
        level_rect = level_text.get_rect(topleft=(bg_rect.x + 7, bg_rect.y - 1))

        pygame.draw.rect(self.screen, COLORS['INDIGO'], bg_rect)
        self.screen.blit(icon_text, icon_rect)
        self.screen.blit(level_text, level_rect)

    def update(self, level):
        self.draw_energy()
        self.draw_lives()
        self.draw_score()
        self.draw_lowest_hi_score()
        self.draw_levels(level)
