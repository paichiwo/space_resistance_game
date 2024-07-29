from src.config import *


class MainMenu:
    def __init__(self, screen, window, states, sound_manager, restart_game):
        self.screen = screen
        self.window = window
        self.states = states
        self.sound_manager = sound_manager
        self.restart_game = restart_game

        self.scale = SCALE
        self.volume_level = 50
        self.options_selected = False
        self.fullscreen = False

        self.menu_items = {
            'main': ['start game', 'options'],
            'options': ['scale', 'fullscreen', f'volume: {self.volume_level}', 'accept']
        }

        self.rects = {
            'main': {item: pygame.rect.Rect() for item in self.menu_items['main']},
            'options': {item: pygame.rect.Rect() for item in self.menu_items['options']}
        }

        self.selected_index = 0
        self.navigate_delay = 200
        self.button_delay = 200
        self.last_navigate_time = pygame.time.get_ticks()
        self.last_button_time = pygame.time.get_ticks()

    def draw_menu(self, items):
        if self.options_selected:
            self.draw_volume_bar()

        x = WIDTH // 2
        y = 180
        for index, item in enumerate(items):
            item_color = COLORS['GREEN'] if index == self.selected_index else COLORS['WHITE']
            text = FONT10.render(item, True, item_color)
            rect = text.get_rect(center=(x, y))
            self.rects['main' if not self.options_selected else 'options'][item] = rect
            self.screen.blit(text, rect)
            y += 10

    def draw_volume_bar(self):
        max_width = 102
        height = 11
        border_color = COLORS['WHITE']
        fill_color = COLORS['GREEN']

        bg_rect = pygame.rect.Rect(WIDTH // 2 - max_width // 2, HEIGHT // 2 + 69, max_width, height)
        pygame.draw.rect(self.screen, border_color, bg_rect, 1)

        fg_rect = pygame.rect.Rect(bg_rect.x + 2, bg_rect.y + 2, (max_width - 4) * self.volume_level / 100, height - 4)
        pygame.draw.rect(self.screen, fill_color, fg_rect)

        self.menu_items['options'][2] = f'volume: {self.volume_level}'

    def input(self, event):
        current_time = pygame.time.get_ticks()

        if event.type == pygame.JOYHATMOTION:
            if current_time - self.last_navigate_time > self.navigate_delay:
                if event.value[1] == 1:  # Up
                    self.selected_index = (self.selected_index - 1) % len(self.current_items())
                elif event.value[1] == -1:  # Down
                    self.selected_index = (self.selected_index + 1) % len(self.current_items())
                self.last_navigate_time = current_time

        if event.type == pygame.JOYAXISMOTION:
            if current_time - self.last_navigate_time > self.navigate_delay:
                if abs(event.value) > 0.5:
                    if event.axis == 1:
                        if event.value > 0:
                            self.selected_index = (self.selected_index + 1) % len(self.current_items())
                        else:
                            self.selected_index = (self.selected_index - 1) % len(self.current_items())
                        self.last_navigate_time = current_time

        if event.type == pygame.JOYBUTTONDOWN:
            if current_time - self.last_button_time > self.button_delay:
                if event.button == 0:
                    self.action(list(self.current_items().keys())[self.selected_index])
                    self.last_button_time = current_time

        if event.type == pygame.KEYDOWN:
            if current_time - self.last_navigate_time > self.navigate_delay:
                if event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.current_items())
                elif event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.current_items())
                if f'volume: {self.volume_level}' in self.current_items():
                    if event.key == pygame.K_LEFT:
                        self.adjust_volume(-1)
                    elif event.key == pygame.K_RIGHT:
                        self.adjust_volume(+1)
                self.last_navigate_time = current_time

            elif current_time - self.last_button_time > self.button_delay:
                if event.key == pygame.K_RETURN:
                    self.action(list(self.current_items().keys())[self.selected_index])
                self.last_button_time = current_time

        if event.type == pygame.MOUSEBUTTONDOWN:
            for item, rect in self.current_items().items():
                if rect and rect.collidepoint(event.pos):
                    self.action(item)

        if event.type == pygame.MOUSEMOTION:
            for index, (item, rect) in enumerate(self.current_items().items()):
                if rect.collidepoint(event.pos):
                    self.selected_index = index
                    break

    def adjust_volume(self, change):
        self.volume_level = max(0, min(100, self.volume_level + change))
        # self.sound_manager.set_volume(self.volume_level / 100)

    def handle_volume_level(self):
        pass

    def action(self, item):
        if item == 'start game':
            self.states['welcome_screen_running'] = False
            self.restart_game()
            self.states['game_running'] = True

        elif item == 'options':
            self.options_selected = True
            self.selected_index = 0
        elif item == 'scale':
            self.scale += 1
            if self.scale >= 5:
                self.scale = 1
            self.window.size = (WIDTH * self.scale, HEIGHT * self.scale)
        elif item == 'fullscreen':
            self.fullscreen = not self.fullscreen
            self.window.set_fullscreen(True) if self.fullscreen else self.window.set_windowed()

        elif item == f'volume: {self.volume_level}':
            self.handle_volume_level()

        elif item == 'accept':
            self.options_selected = False
            self.selected_index = 0

    def current_items(self):
        return self.rects['options'] if self.options_selected else self.rects['main']

    def update(self, event):
        self.input(event)
        self.draw_menu(self.menu_items['options'] if self.options_selected else self.menu_items['main'])
