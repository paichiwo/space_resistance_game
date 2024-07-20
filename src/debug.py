from src.config import *


class DebugMenu:
    def __init__(self, screen, level_manager, states):
        self.screen = screen
        self.level_manager = level_manager
        self.states = states

        self.surf = pygame.Surface((WIDTH / 3, HEIGHT))
        self.surf.fill(COLORS['INDIGO'])
        self.surf.set_alpha(200)
        self.rect = self.surf.get_rect(topright=(WIDTH, 0))

        self.debug_items = {
            'god mode': False,
            'level': 1,
            'main menu': True,
            'game run': False,
            'game over': False,
            'congrats': False
        }

        self.start_time = pygame.time.get_ticks()
        self.item_positions = []

    def draw_bg(self):
        self.screen.blit(self.surf, self.rect)

    def draw_title(self):
        title_text = FONT10.render('DEBUG MENU:', True, COLORS['GOLD'])
        title_rect = title_text.get_rect(center=(215, 15))
        self.screen.blit(title_text, title_rect)

    def draw_text(self):
        self.item_positions.clear()
        mouse_pos = (pygame.mouse.get_pos()[0] // SCALE, pygame.mouse.get_pos()[1] // SCALE)

        x = 198
        y = 30
        self.draw_title()
        for item, state in self.debug_items.items():
            item_color = COLORS['GOLD'] if pygame.font.Font.render(FONT10, item, True, COLORS['YELLOW']).get_rect(
                center=(x, y)).collidepoint(mouse_pos) else COLORS['YELLOW']
            state_color = COLORS['RED'] if not state else COLORS['GREEN']

            item_text = FONT10.render(item, True, item_color)
            state_text = FONT10.render(str(state), True, state_color)

            item_rect = item_text.get_rect(center=(x, y))
            state_rect = state_text.get_rect(center=(x + 42, y))

            self.screen.blit(item_text, item_rect)
            self.screen.blit(state_text, state_rect)

            self.item_positions.append((item, item_rect))
            y += 10

    def input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for item, item_rect in self.item_positions:
                if item_rect.collidepoint(event.pos):
                    self.toggle_items(item)

    def toggle_items(self, item):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > 200:

            if item == 'main menu':
                self.states['welcome_screen_running'] = not self.states['welcome_screen_running']
                self.debug_items['main menu'] = self.states['welcome_screen_running']
                self.states['game_running'] = False
                self.states['game_over_screen_running'] = False
                self.states['congrats_screen_running'] = False

            elif item == 'game run':
                self.states['welcome_screen_running'] = False
                self.states['game_running'] = not self.states['game_running']
                self.debug_items['game run'] = self.states['game_running']
                self.states['game_over_screen_running'] = False
                self.states['congrats_screen_running'] = False

            elif item == 'game over':
                self.states['welcome_screen_running'] = False
                self.states['game_running'] = False
                self.states['game_over_screen_running'] = not self.states['game_over_screen_running']
                self.debug_items['game over'] = self.states['game_over_screen_running']
                self.states['congrats_screen_running'] = False

            elif item == 'congrats':
                self.states['welcome_screen_running'] = False
                self.states['game_running'] = False
                self.states['game_over_screen_running'] = False
                self.states['congrats_screen_running'] = not self.states['congrats_screen_running']
                self.debug_items['congrats'] = self.states['congrats_screen_running']

            elif item == 'god mode':
                self.debug_items[item] = not self.debug_items[item]

            elif item == 'level':
                self.debug_items[item] += 1
                if self.debug_items[item] > 4:
                    self.debug_items[item] = 1

            self.start_time = pygame.time.get_ticks()

    def set_in_game(self):
        self.level_manager.player.god_mode = self.debug_items['god mode']

        new_level_index = self.debug_items['level'] - 1
        if new_level_index != self.level_manager.level_index:
            self.level_manager.level_index = new_level_index
            self.level_manager.change_bg(new_level_index)

    def update(self, event):
        self.draw_bg()
        self.draw_text()
        self.input(event)
        self.set_in_game()
