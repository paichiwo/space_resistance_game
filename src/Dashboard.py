import pygame
import time

class DashBoard:
    """Creates a dashboard object containing game statistics"""

    def __init__(self, screen, clock, game_start_time, screen_width):
        super().__init__()

        self.screen = screen
        self.clock = clock
        self.game_start_time = game_start_time
        self.screen_width = screen_width
        self.start_time = time.time()

        self.font_color = "White"
        self.font = pygame.font.Font("font/pixela_regular.ttf", 14)
        self.font_bold = pygame.font.Font("font/pixela_bold.ttf", 14)

        self.headers = ["TIME", "SPEED", "DIST", "FPS"]
        self.header_x_positions = [20, 120, 440, 540]
        self.header_y_pos = 740
        self.data_y_pos = 770

        self.distance = 0

    def draw_background_and_headers(self):
        """Draw a dashboard background and headers"""
        pygame.draw.rect(self.screen, "white", pygame.Rect(0, 728, 600, 2))
        pygame.draw.rect(self.screen, "black", pygame.Rect(0, 730, 600, 70))

        text_list = [self.font_bold.render(header, 0, self.font_color) for header in self.headers]
        for i, text in enumerate(text_list):
            self.screen.blit(text, (self.header_x_positions[i], 740))

    def show_time(self):
        """Display elapsed time information"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.game_start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = "{:02}:{:02}".format(minutes, seconds)
        time_text = self.font.render(timer_text, 0, self.font_color)
        self.screen.blit(time_text, (self.header_x_positions[0], self.data_y_pos))

    def show_speed(self, speed):
        """Display speed information"""
        speed_text = self.font.render(f"{speed} km/h", 0, self.font_color)
        self.screen.blit(speed_text, (self.header_x_positions[1]-2, self.data_y_pos))

    def show_distance(self, speed, acceleration):
        """Display distance information"""
        current_time = time.time()
        delta_time_seconds = (current_time - self.start_time) * 0.000278
        delta_distance = speed * delta_time_seconds + (acceleration * delta_time_seconds ** 2) / 2
        self.distance += delta_distance
        self.start_time = current_time
        distance_text = self.font.render("{:.2f} km".format(self.distance), 0, self.font_color)
        self.screen.blit(distance_text, (self.header_x_positions[2]-10, self.data_y_pos))

    def show_fps(self):
        """Display the current FPS rate"""
        fps_text = self.font.render("{:.2f}".format(self.clock.get_fps()), 0, self.font_color)
        self.screen.blit(fps_text, (self.header_x_positions[3]-5, self.data_y_pos))

    def update(self, speed, acceleration):
        self.draw_background_and_headers()
        self.show_time()
        self.show_speed(speed)
        self.show_distance(speed, acceleration)
        self.show_fps()
