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
                        f'volume: {self.volume_level}', 'accept'],
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
        width = 102
        height = 11

        selected = (self.selected_index == self.menu_items['options'].index(f'volume: {self.volume_level}'))

        # bar
        self.rects['volume']['main'] = pygame.rect.Rect(WIDTH // 2 - width // 2,
                                                        HEIGHT // 2 + 69,
                                                        width,
                                                        height)
        self.rects['volume']['inside'] = pygame.rect.Rect(self.rects['volume']['main'].x + 2,
                                                          self.rects['volume']['main'].y + 2,
                                                          (width - 4) * self.volume_level / 100,
                                                          height - 4)
        # draw bar
        pygame.draw.rect(self.screen, COLORS['INDIGO'] if selected else COLORS['WHITE'],
                         self.rects['volume']['main'], 1)
        pygame.draw.rect(self.screen, COLORS['INDIGO'], self.rects['volume']['inside'])

        # buttons
        self.rects['volume']['minus'] = pygame.rect.Rect(self.rects['volume']['main'].x - height - 1,
                                                         self.rects['volume']['main'].y,
                                                         height,
                                                         height)
        self.rects['volume']['plus'] = pygame.rect.Rect(self.rects['volume']['main'].x + width + 1,
                                                        self.rects['volume']['main'].y,
                                                        height,
                                                        height)

        # draw button effect
        minus_color = self.get_button_color('minus')
        plus_color = self.get_button_color('plus')
        pygame.draw.rect(self.screen, minus_color, self.rects['volume']['minus'])
        pygame.draw.rect(self.screen, plus_color, self.rects['volume']['plus'])

        # draw buttons
        pygame.draw.rect(self.screen, COLORS['WHITE'], self.rects['volume']['minus'], 1)
        pygame.draw.rect(self.screen, COLORS['WHITE'], self.rects['volume']['plus'], 1)

        minus_text = FONT10.render('-', True, COLORS['WHITE'])
        plus_text = FONT10.render('+', True, COLORS['WHITE'])

        self.screen.blit(minus_text, minus_text.get_rect(center=(self.rects['volume']['main'].x - 6,
                                                                 self.rects['volume']['main'].y + 6)))
        self.screen.blit(plus_text, plus_text.get_rect(center=(self.rects['volume']['main'].x + width + 7,
                                                               self.rects['volume']['main'].y + 6)))

    def input(self, event):
        current_time = pygame.time.get_ticks()

        if event.type == pygame.JOYHATMOTION:
            if current_time - self.last_navigate_time > self.navigate_delay:
                if event.value[1] == 1:
                    self.selected_index = (self.selected_index - 1) % len(self.current_items())
                elif event.value[1] == -1:
                    self.selected_index = (self.selected_index + 1) % len(self.current_items())
                elif event.value[0] == -1 and 'volume: ' in self.menu_items['options'][self.selected_index]:
                    self.adjust_volume(-1)
                    self.start_button_effect('minus')
                elif event.value[0] == 1 and 'volume: ' in self.menu_items['options'][self.selected_index]:
                    self.adjust_volume(1)
                    self.start_button_effect('plus')
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
                    elif event.axis == 0:
                        if self.selected_index == self.menu_items['options'].index(f'volume: {self.volume_level}'):
                            if event.value < 0:
                                self.adjust_volume(-1)
                                self.start_button_effect('minus')
                            else:
                                self.adjust_volume(1)
                                self.start_button_effect('plus')
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
                if self.selected_index == self.menu_items['options'].index(f'volume: {self.volume_level}'):
                    if event.key == pygame.K_LEFT:
                        self.adjust_volume(-1)
                        self.start_button_effect('minus')
                    elif event.key == pygame.K_RIGHT:
                        self.adjust_volume(1)
                        self.start_button_effect('plus')
                self.last_navigate_time = current_time

            if current_time - self.last_button_time > self.button_delay:
                if event.key == pygame.K_RETURN:
                    self.action(list(self.current_items().keys())[self.selected_index])
                self.last_button_time = current_time

        if event.type == pygame.MOUSEMOTION:
            for index, (item, rect) in enumerate(self.current_items().items()):
                if rect.collidepoint(event.pos):
                    self.selected_index = index
                    break

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_time - self.last_button_time > self.button_delay:
                for item, rect in self.current_items().items():
                    if rect and rect.collidepoint(event.pos):
                        self.action(item)
                        self.last_button_time = current_time
                        break

                if self.selected_index == self.menu_items['options'].index(f'volume: {self.volume_level}'):
                    if self.rects['volume']['minus'].collidepoint(event.pos):
                        self.adjust_volume(-1)
                        self.start_button_effect('minus')
                    elif self.rects['volume']['plus'].collidepoint(event.pos):
                        self.adjust_volume(1)
                        self.start_button_effect('plus')
                self.last_button_time = current_time

    def adjust_volume(self, change):
        self.volume_level = max(0, min(100, self.volume_level + change))
        self.sound_manager.set_master_volume(self.volume_level / 100)
        self.menu_items['options'][2] = f'volume: {self.volume_level}'

    def action(self, item):
        current_time = pygame.time.get_ticks()
        if current_time - self.action_time > self.action_delay:
            if item == 'start game':
                self.states['welcome_screen_running'] = False
                self.restart_game()
                self.states['game_running'] = True

            elif item == 'options':
                self.options_selected = True
                self.selected_index = 0

            elif item.startswith('scale'):
                self.scale += 1
                if self.scale >= 5:
                    self.scale = 1
                self.menu_items['options'][0] = f'scale: {self.scale}'
                self.window.size = (WIDTH * self.scale, HEIGHT * self.scale)

            elif item.startswith('fullscreen'):
                self.fullscreen = not self.fullscreen
                self.window.set_fullscreen(True) if self.fullscreen else self.window.set_windowed()
                self.menu_items['options'][1] = f'fullscreen: {"yes" if self.fullscreen else "no"}'

            elif item == 'accept':
                self.options_selected = False
                self.selected_index = 0

            self.action_time = current_time

    def current_items(self):
        return self.rects['options'] if self.options_selected else self.rects['main']

    def get_button_color(self, button_type):
        base_color = COLORS['BLACK']
        target_color = COLORS['INDIGO']
        duration = 100

        if self.button_interaction_state == button_type:
            elapsed_time = pygame.time.get_ticks() - self.button_interaction_time
            if elapsed_time > duration:
                self.button_interaction_state = None
                return base_color

            t = (elapsed_time / duration)

            return (
                int(base_color[0] * (1 - t) + target_color[0] * t),
                int(base_color[1] * (1 - t) + target_color[1] * t),
                int(base_color[2] * (1 - t) + target_color[2] * t),
            )

        return base_color

    def start_button_effect(self, button_type):
        self.button_interaction_state = button_type
        self.button_interaction_time = pygame.time.get_ticks()

    def update(self, event):
        self.input(event)
        self.draw_menu(self.menu_items['options'] if self.options_selected else self.menu_items['main'])
