import sys
import pygame
from src.background import Background


class Game:

    def __init__(self):
        super().__init__()

        # Game constants
        self.window_width = 320
        self.window_height = 180
        self.fps = 60

        # Game setup
        pygame.init()
        pygame.display.set_caption("pyshump")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()

        self.bg = Background(self.screen, self.window_height)

        self.running = True

    def handle_events(self, event):
        """Handle game events"""
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if self.running:
            pass

    def update_game(self):
        """Update all game objects"""
        self.screen.fill("black")
        self.bg.update()

    def game_loop(self):
        while True:

            for event in pygame.event.get():
                self.handle_events(event)
            if self.running:
                self.update_game()

            pygame.display.flip()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    Game().run()
