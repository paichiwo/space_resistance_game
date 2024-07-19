import pygame

from src.config import *
from src.timer import Timer


class DebugMenu:
    def __init__(self, screen, level_manager):
        self.screen = screen
        self.level_manager = level_manager

        self.surf = pygame.Surface((WIDTH / 3, HEIGHT))
        self.surf.fill('indigo')
        self.rect = self.surf.get_rect(topright=(WIDTH, 0))

        self.debug_items = {
            'god mode': False,
            'level': 1
        }

        self.start_time = pygame.time.get_ticks()

        self.item_positions = []

    def draw_bg(self):
        self.screen.blit(self.surf, self.rect)

    def draw_text(self):
        x = 198
        y = 10
        for item, state in self.debug_items.items():
            text = FONT10.render(item, True, 'yellow')
            item_rect = text.get_rect(center=(x, y))
            self.screen.blit(text, item_rect)

            text = FONT10.render(str(state), True, 'red')
            state_rect = text.get_rect(center=(x + 42, y))
            self.screen.blit(text, state_rect)

            self.item_positions.append((item, item_rect))
            pygame.draw.rect(self.screen, 'white', item_rect, 1)

            y += 10

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for item, item_rect in self.item_positions:
                if item_rect.collidepoint(mouse_pos):
                    self.toggle_item(item)

    def toggle_item(self, item):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > 200:

            if item == 'god mode':
                self.debug_items[item] = not self.debug_items[item]
            elif item == 'level':
                self.debug_items[item] += 1
                if self.debug_items[item] > 4:
                    self.debug_items[item] = 1

            self.start_time = pygame.time.get_ticks()

    def update(self, event):
        self.draw_bg()
        self.draw_text()
        self.input(event)
