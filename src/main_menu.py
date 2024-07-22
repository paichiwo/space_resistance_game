from src.config import *


class MainMenu:
    def __init__(self, screen, window, states, sound_manager):
        self.screen = screen
        self.window = window
        self.states = states
        self.sound_manager = sound_manager

        self.main_menu_items = {
            'start game': pygame.rect.Rect(),
            'options': pygame.rect.Rect()
        }

        self.options_items = {
            'scale': pygame.rect.Rect(),
            'fullscreen': pygame.rect.Rect(),
            'volume': pygame.rect.Rect(),
            'accept': pygame.rect.Rect()
        }

        self.start_time = pygame.time.get_ticks()
        self.options = False
        self.scale = SCALE

    def draw_main_menu(self):
        mouse_pos = (pygame.mouse.get_pos()[0] // self.scale, pygame.mouse.get_pos()[1] // self.scale)

        x = WIDTH // 2
        y = 180
        for item in self.main_menu_items.keys():
            item_color = COLORS['GREEN'] if pygame.font.Font.render(FONT10, item, True, COLORS['WHITE']).get_rect(
                center=(x, y)).collidepoint(mouse_pos) else COLORS['WHITE']
            text = FONT10.render(item, True, item_color)
            rect = text.get_rect(center=(x, y))
            self.main_menu_items[item] = rect
            self.screen.blit(text, rect)
            y += 10

    def draw_options_menu(self):
        mouse_pos = (pygame.mouse.get_pos()[0] // self.scale, pygame.mouse.get_pos()[1] // self.scale)

        x = WIDTH // 2
        y = 180
        for item in self.options_items.keys():
            item_color = COLORS['GREEN'] if pygame.font.Font.render(FONT10, item, True, COLORS['WHITE']).get_rect(
                center=(x, y)).collidepoint(mouse_pos) else COLORS['WHITE']
            text = FONT10.render(item, True, item_color)
            rect = text.get_rect(center=(x, y))
            self.options_items[item] = rect
            self.screen.blit(text, rect)
            y += 10

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.options:
                for item, rect in self.main_menu_items.items():
                    if rect and rect.collidepoint(event.pos):
                        self.action(item)
            else:
                for item, rect in self.options_items.items():
                    if rect and rect.collidepoint(event.pos):
                        self.action(item)

    def action(self, item):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > 200:

            if item == 'start game':
                self.states['welcome_screen_running'] = False
                self.states['game_running'] = True
            elif item == 'options':
                self.options = True
            elif item == 'scale':

                self.scale += 1
                if self.scale >= 5:
                    self.scale = 1
                print(self.scale)
                self.window.size = (WIDTH * self.scale, HEIGHT * self.scale)

            elif item == 'accept':
                self.options = False

            self.start_time = pygame.time.get_ticks()

    def update(self, event):
        self.input(event)
        if self.options:
            self.draw_options_menu()
        else:
            self.draw_main_menu()
