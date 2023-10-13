import pygame


class Dashboard:
    def __init__(self, screen):
        super().__init__()

        self.screen = screen

        self.logo_img = pygame.image.load("assets/img/ui/pyshmup_logo.png").convert_alpha()
        self.rect = self.logo_img.get_rect(midtop=(289, 12))

    def draw_dashboard_bg(self):
        pygame.draw.rect(self.screen, "black", pygame.Rect(256, 0, 64, 180))

    def draw_logo(self):
        self.screen.blit(self.logo_img, self.rect)

    def update(self):
        self.draw_dashboard_bg()
        self.draw_logo()
