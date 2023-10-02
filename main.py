import sys
import pygame
from src.Road import Road
from src.Player import Player
from src.Dashboard import DashBoard


class Game:

    def __init__(self):
        super().__init__()

        self.window_width = 600
        self.window_height = 800
        self.fps = 60

        pygame.init()
        pygame.display.set_caption("Racing Game")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font("font/joystix_mono.otf", 18)
        self.start_time = pygame.time.get_ticks()

        # Create game objects
        self.road = Road(self.screen, self.window_height)
        self.dashboard = DashBoard(self.screen, self.clock, self.start_time)
        self.player = pygame.sprite.GroupSingle(Player())

        self.running = True

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.running:
                self.road.update()
                self.player.draw(self.screen)
                self.player.update()
                self.dashboard.update(self.road.speed, self.road.distance)

            pygame.display.update()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    Game().run()
