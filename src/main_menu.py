from src.config import *


class MainMenu:
    def __init__(self, screen):
        self.screen = screen

        self.items = {
            'start game': pygame.rect.Rect(),
            'options': pygame.rect.Rect()
        }

    def draw(self):
        mouse_pos = (pygame.mouse.get_pos()[0] // SCALE, pygame.mouse.get_pos()[1] // SCALE)

        x = WIDTH // 2
        y = 180
        for item in self.items.keys():
            item_color = COLORS['GREEN'] if pygame.font.Font.render(FONT10, item, True, COLORS['WHITE']).get_rect(
                center=(x, y)).collidepoint(mouse_pos) else COLORS['WHITE']
            text = FONT10.render(item, True, item_color)
            rect = text.get_rect(center=(x, y))
            self.items[item] = rect
            self.screen.blit(text, rect)
            y += 10

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item, rect in self.items.items():
                if rect and rect.collidepoint(event.pos):
                    print(f'{item} selected')

    def update(self, event):
        self.draw()
        self.input(event)
