from src.config import *


class MainMenu:
    def __init__(self, screen, window, states, sound_manager, restart_game):
        self.screen = screen
        self.window = window
        self.states = states
        self.sound_manager = sound_manager
        self.restart_game = restart_game
        self.scale = SCALE

        self.selected_index = 0
        self.navigate_delay = 200
        self.button_delay = 200
        self.action_delay = 200
        self.last_navigate_time = pygame.time.get_ticks()
        self.last_button_time = pygame.time.get_ticks()
        self.action_time = pygame.time.get_ticks()
        self.button_interaction_state = None
        self.button_interaction_time = 0
        self.volume_level = 50
        self.options_selected = False
        self.fullscreen = False

        self.menu_items = {
            'main': ['start game', 'options'],
            'options': [f'scale: {self.scale}',
                        f'fullscreen: {"yes" if self.fullscreen else "no"}',
                        f'volume: {self.volume_level}',
                        'accept'],
            'volume': ['main', 'inside', 'minus', 'plus']
        }
        self.rects = {
            'main': {item: pygame.rect.Rect() for item in self.menu_items['main']},
            'options': {item: pygame.rect.Rect() for item in self.menu_items['options']},
            'volume': {item: pygame.rect.Rect() for item in self.menu_items['volume']}
        }

    def draw_menu(self, items):
        if self.options_selected:
            self.draw_volume_bar()

        x = WIDTH // 2
        y = 180
        for index, item in enumerate(items):
            if item == f'volume: {self.volume_level}':
                item_color = COLORS['WHITE']
            else:
                item_color = COLORS['INDIGO'] if index == self.selected_index else COLORS['WHITE']
            text = FONT10.render(item, True, item_color)
            rect = text.get_rect(center=(x, y))
            self.rects['main' if not self.options_selected else 'options'][item] = rect
            self.screen.blit(text, rect)
            y += 10

    def draw_volume_bar(self):
        width, height = 102, 11
        selected_index = self.menu_items['options'].index(f'volume: {self.volume_level}')
        selected = self.selected_index == selected_index

        # Get the rect for the volume item
        volume_item_rect = list(self.rects['options'].values())[2]

        # Bar rects
        main_rect = pygame.rect.Rect(volume_item_rect.x - width // 4 + 2, volume_item_rect.y - 1, width, height)
        inside_rect = pygame.rect.Rect(main_rect.x + 2, main_rect.y + 2, (width - 4) * self.volume_level / 100,
                                       height - 4)
        # Button rects
        minus_rect = pygame.rect.Rect(main_rect.x - height - 1, main_rect.y, height, height)
        plus_rect = pygame.rect.Rect(main_rect.x + width + 1, main_rect.y, height, height)

        # Draw bar
        pygame.draw.rect(self.screen, COLORS['INDIGO'] if selected else COLORS['WHITE'], main_rect, 1)
        pygame.draw.rect(self.screen, COLORS['INDIGO'], inside_rect)

        # Draw buttons
        pygame.draw.rect(self.screen, self.get_button_color('minus'), minus_rect)
        pygame.draw.rect(self.screen, self.get_button_color('plus'), plus_rect)
        pygame.draw.rect(self.screen, COLORS['WHITE'], minus_rect, 1)
        pygame.draw.rect(self.screen, COLORS['WHITE'], plus_rect, 1)

        # Draw button texts
        minus_text = FONT10.render('-', True, COLORS['WHITE'])
        plus_text = FONT10.render('+', True, COLORS['WHITE'])
        self.screen.blit(minus_text, minus_text.get_rect(center=(minus_rect.centerx + 1, minus_rect.centery + 1)))
        self.screen.blit(plus_text, plus_text.get_rect(center=(plus_rect.centerx + 1, plus_rect.centery + 1)))

        # Update rects
        self.rects['volume'] = {'main': main_rect, 'inside': inside_rect, 'minus': minus_rect, 'plus': plus_rect}

    def input(self, event):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_navigate_time > self.navigate_delay:
            if event.type == pygame.JOYHATMOTION:
                self.handle_joystick_hat_motion(event)
            elif event.type == pygame.JOYAXISMOTION:
                self.handle_joystick_axis_motion(event)
            elif event.type == pygame.KEYDOWN:
                self.handle_key_down(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_button_down(event)

    def handle_joystick_hat_motion(self, event):
        if event.value[1] == 1:
            self.update_selection(-1)
        elif event.value[1] == -1:
            self.update_selection(1)
        elif event.value[0] in (-1, 1) and 'volume: ' in self.menu_items['options'][self.selected_index]:
            self.adjust_volume(-1 if event.value[0] == -1 else 1)
            self.start_button_effect('minus' if event.value[0] == -1 else 'plus')
        self.last_navigate_time = pygame.time.get_ticks()

    def handle_joystick_axis_motion(self, event):
        if abs(event.value) > 0.5:
            if event.axis == 1:
                self.update_selection(1 if event.value > 0 else -1)
            elif event.axis == 0 and self.selected_index == self.menu_items['options'].index(
                    f'volume: {self.volume_level}'):
                self.adjust_volume(-1 if event.value < 0 else 1)
                self.start_button_effect('minus' if event.value < 0 else 'plus')
        self.last_navigate_time = pygame.time.get_ticks()

    def handle_key_down(self, event):
        if event.key == pygame.K_DOWN:
            self.update_selection(1)
        elif event.key == pygame.K_UP:
            self.update_selection(-1)
        elif event.key == pygame.K_LEFT and self.selected_index == self.menu_items['options'].index(
                f'volume: {self.volume_level}'):
            self.adjust_volume(-1)
            self.start_button_effect('minus')
        elif event.key == pygame.K_RIGHT and self.selected_index == self.menu_items['options'].index(
                f'volume: {self.volume_level}'):
            self.adjust_volume(1)
            self.start_button_effect('plus')
        elif event.key == pygame.K_RETURN:
            self.perform_action()
        self.last_navigate_time = pygame.time.get_ticks()

    def handle_mouse_motion(self, event):
        for index, (item, rect) in enumerate(self.current_items().items()):
            if rect.collidepoint(event.pos):
                self.selected_index = index
                break

    def handle_mouse_button_down(self, event):
        if pygame.time.get_ticks() - self.last_button_time > self.button_delay:
            for item, rect in self.current_items().items():
                if rect.collidepoint(event.pos):
                    self.perform_action()
                    self.last_button_time = pygame.time.get_ticks()
                    break

            if self.selected_index == self.menu_items['options'].index(f'volume: {self.volume_level}'):
                if self.rects['volume']['minus'].collidepoint(event.pos):
                    self.adjust_volume(-1)
                    self.start_button_effect('minus')
                elif self.rects['volume']['plus'].collidepoint(event.pos):
                    self.adjust_volume(1)
                    self.start_button_effect('plus')
            self.last_button_time = pygame.time.get_ticks()

    def update_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(self.current_items())

    def perform_action(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.action_time > self.action_delay:
            item = list(self.current_items().keys())[self.selected_index]
            if item == 'start game':
                self.states['welcome_screen_running'] = False
                self.restart_game()
                self.states['game_running'] = True
            elif item == 'options':
                self.options_selected = True
                self.selected_index = 0
            elif item.startswith('scale'):
                self.scale = (self.scale % 4) + 1
                self.menu_items['options'][0] = f'scale: {self.scale}'
                self.window.size = (WIDTH * self.scale, HEIGHT * self.scale)
            elif item.startswith('fullscreen'):
                self.fullscreen = not self.fullscreen
                self.window.set_fullscreen(self.fullscreen) if self.fullscreen else self.window.set_windowed()
                self.menu_items['options'][1] = f'fullscreen: {"yes" if self.fullscreen else "no"}'
            elif item == 'accept':
                self.options_selected = False
                self.selected_index = 0
            self.action_time = current_time

    def adjust_volume(self, change):
        self.volume_level = max(0, min(100, self.volume_level + change))
        self.sound_manager.set_master_volume(self.volume_level / 100)
        self.menu_items['options'][2] = f'volume: {self.volume_level}'

    def current_items(self):
        return self.rects['options'] if self.options_selected else self.rects['main']

    def get_button_color(self, button_type):
        if self.button_interaction_state != button_type:
            return COLORS['BLACK']

        elapsed_time = pygame.time.get_ticks() - self.button_interaction_time
        duration = 100

        if elapsed_time > duration:
            self.button_interaction_state = None
            return COLORS['BLACK']

        t = min(elapsed_time / duration, 1)
        return tuple(int(COLORS['BLACK'][i] * (1 - t) + COLORS['INDIGO'][i] * t) for i in range(3))

    def start_button_effect(self, button_type):
        self.button_interaction_state = button_type
        self.button_interaction_time = pygame.time.get_ticks()

    def update(self, event):
        self.input(event)
        self.draw_menu(self.menu_items['options'] if self.options_selected else self.menu_items['main'])
