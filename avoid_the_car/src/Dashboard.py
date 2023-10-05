import pygame


class DashBoard:
    """Creates a dashboard object containing game statistics"""

    def __init__(self, screen, clock, game_start_time, screen_width):
        super().__init__()

        self.screen = screen
        self.clock = clock
        self.screen_width = screen_width
        self.start_time = pygame.time.get_ticks()

        self.font_color = "White"
        self.font = pygame.font.Font("font/pixela_regular.ttf", 14)
        self.font_bold = pygame.font.Font("font/pixela_bold.ttf", 14)

        self.headers = ["TIME", "SPEED", "SCORE", "DIST", "FPS"]
        self.header_x_positions = [20, 110, 220, 440, 540]
        self.header_y_pos = 740
        self.data_y_pos = 770

        self.score = 0
        self.level = 1
        self.distance = 0

    def draw_background_and_headers(self):
        """Draw a dashboard background and headers"""
        pygame.draw.rect(self.screen, "white", pygame.Rect(0, 728, 600, 2))
        pygame.draw.rect(self.screen, "black", pygame.Rect(0, 730, 600, 70))

        text_list = [self.font_bold.render(header, 0, self.font_color) for header in self.headers]
        for i, text in enumerate(text_list):
            self.screen.blit(text, (self.header_x_positions[i], 740))

    def show_speed(self, speed):
        """Display speed information"""
        speed_text = self.font.render("{} km/h".format(speed), 0, self.font_color)
        self.screen.blit(speed_text, (self.header_x_positions[1]-2, self.data_y_pos))

    def show_level(self):
        """Count and display level information"""
        self.level = int(self.distance)+1
        print(self.distance)
        level_text = self.font.render("Level: {}".format(self.level), 0, self.font_color)
        self.screen.blit(level_text, (330, 750))

    def show_score(self, obstacle_y_pos):
        """Count and display score information"""
        if obstacle_y_pos >= 702:
            self.score += 1
        score_text = self.font.render("{}".format("{:06}".format(self.score)), 0, self.font_color)
        self.screen.blit(score_text, (self.header_x_positions[2], self.data_y_pos))

    def show_distance(self, speed):
        """Display distance information"""
        current_time = pygame.time.get_ticks()
        delta_time_seconds = (current_time - self.start_time) * 0.000000278
        delta_distance = speed * delta_time_seconds
        self.distance += delta_distance
        self.start_time = current_time
        distance_text = self.font.render("{:.2f} km".format(self.distance), 0, self.font_color)
        self.screen.blit(distance_text, (self.header_x_positions[3]-10, self.data_y_pos))

    def show_fps(self):
        """Display the current FPS rate"""
        fps_text = self.font.render("{:.2f}".format(self.clock.get_fps()), 0, self.font_color)
        self.screen.blit(fps_text, (self.header_x_positions[4]-5, self.data_y_pos))

    def reset(self):
        self.score = 0
        self.start_time = pygame.time.get_ticks()
        self.level = 1
        self.distance = 0

    def update(self, speed, obstacle_y_pos):
        self.draw_background_and_headers()
        self.show_speed(speed)
        self.show_level()
        self.show_score(obstacle_y_pos)
        self.show_distance(speed)
        self.show_fps()
