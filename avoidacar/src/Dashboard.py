import pygame


class DashBoard:
    """Creates a dashboard object containing game statistics"""

    def __init__(self, screen, clock, screen_width):
        super().__init__()

        self.screen = screen
        self.clock = clock
        self.screen_width = screen_width
        self.start_time = pygame.time.get_ticks()

        self.font_color = "White"
        self.font = pygame.font.Font("font/pixela_regular.ttf", 14)
        self.font_bold = pygame.font.Font("font/pixela_bold.ttf", 14)

        self.headers = ["DIST", "SPEED", "SCORE", "FPS"]
        self.header_x_positions = [90, 170, 365, 470]
        self.level_x_pos = 270
        self.header_y_pos = 740
        self.data_y_pos = 770

        self.distance = 0
        self.level = 1
        self.score = 0

    def draw_background_and_headers(self):
        """Draw a dashboard background and headers"""
        pygame.draw.rect(self.screen, "white", pygame.Rect(0, 728, 600, 2))
        pygame.draw.rect(self.screen, "black", pygame.Rect(0, 730, 600, 70))

        text_list = [self.font_bold.render(header, 0, self.font_color) for header in self.headers]
        for i, text in enumerate(text_list):
            self.screen.blit(text, (self.header_x_positions[i], self.header_y_pos))

    def show_distance(self, speed):
        """Display distance information"""
        current_time = pygame.time.get_ticks()
        time = (current_time - self.start_time) * 0.000000278
        distance = speed * time
        self.distance += distance
        self.start_time = current_time
        text = self.font.render("{:.2f}".format(self.distance), 0, self.font_color)
        self.screen.blit(text, (self.header_x_positions[0]+5, self.data_y_pos))

    def show_speed(self, speed):
        """Display speed information"""
        text = self.font.render("{}".format(speed), 0, self.font_color)
        self.screen.blit(text, (self.header_x_positions[1]+20, self.data_y_pos))

    def show_health(self, health, max_health):
        """Display health bar"""
        health_bar_length = 100
        health_ratio = max_health / health_bar_length
        bar_width = health / health_ratio
        pygame.draw.rect(self.screen, "red", pygame.Rect(250, self.header_y_pos, bar_width, 15))
        pygame.draw.rect(self.screen, "white", pygame.Rect(250, self.header_y_pos, health_bar_length, 15), 2)

    def show_level(self):
        """Count and display level information"""
        self.level = int(self.distance)+1
        text = self.font.render("Level: {}".format(self.level), 0, self.font_color)
        self.screen.blit(text, (self.level_x_pos, self.data_y_pos))

    def show_score(self, obstacle_y_pos):
        """Count and display score information"""
        if obstacle_y_pos >= 702:
            self.score += 1
        text = self.font.render("{}".format("{:06}".format(self.score)), 0, self.font_color)
        self.screen.blit(text, (self.header_x_positions[2]+4, self.data_y_pos))

    def show_fps(self):
        """Display the current FPS rate"""
        text = self.font.render("{:.2f}".format(self.clock.get_fps()), 0, self.font_color)
        self.screen.blit(text, (self.header_x_positions[3]-3, self.data_y_pos))

    def reset(self):
        """Reset dashboard values"""
        self.start_time = pygame.time.get_ticks()
        self.distance = 0
        self.level = 1
        self.score = 0

    def update(self, speed, health, max_health, obstacle_y_pos):
        self.draw_background_and_headers()
        self.show_distance(speed)
        self.show_speed(speed)
        self.show_health(health, max_health)
        self.show_level()
        self.show_score(obstacle_y_pos)
        self.show_fps()
