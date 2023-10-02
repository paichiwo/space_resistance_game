import pygame


class DashBoard:
    """Creates a dashboard object containing game statistics"""

    def __init__(self, screen, clock, start_time, font):
        super().__init__()

        self.screen = screen
        self.clock = clock
        self.start_time = start_time
        self.speed = 0
        self.font = font

    def show_speed(self, speed):
        """Display speed information"""
        speed_text = self.font.render(f"{speed} km/h", 1, "Black")
        self.screen.blit(speed_text, (10, 750))

    def show_distance(self, distance):
        """Display distance information"""
        distance_text = self.font.render("{:.2f} km".format(distance), 1, "Black")
        self.screen.blit(distance_text, (10, 700))

    def show_time(self):
        """Display elapsed time information"""
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = "{:02}:{:02}".format(minutes, seconds)
        time_text = self.font.render(timer_text, 1, "Black")
        self.screen.blit(time_text, (460, 700))

    def show_fps_counter(self):
        """Display the current FPS rate"""
        fps = str(round(self.clock.get_fps(), 2))
        fps_text = self.font.render(f"FPS {fps}", 1, "Black")
        self.screen.blit(fps_text, (460, 750))

    def update(self, speed, distance):
        self.show_speed(speed)
        self.show_distance(distance)
        self.show_time()
        self.show_fps_counter()
