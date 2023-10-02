import pygame


class DashBoard:
    def __init__(self, screen, clock, start_time, font):
        super().__init__()

        self.screen = screen
        self.clock = clock
        self.start_time = start_time
        self.font = font

    def show_fps_counter(self):
        """Display the current FPS rate"""
        fps = str(round(self.clock.get_fps(), 2))
        fps_text = self.font.render(f"FPS {fps}", 1, "Black")
        self.screen.blit(fps_text, (460, 750))

    def show_time(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = "{:02}:{:02}".format(minutes, seconds)
        time_text = self.font.render(timer_text, 1, "Black")
        self.screen.blit(time_text, (460, 700))

    def update(self):
        self.show_fps_counter()
        self.show_time()

