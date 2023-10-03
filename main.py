import sys
import pygame
from src.Road import Road
from src.Dashboard import DashBoard
from src.Player import Player
from src.Obstacle import Obstacle


class Game:

    def __init__(self):
        super().__init__()

        # Game constants
        self.window_width = 600
        self.window_height = 800
        self.fps = 60

        # Game setup
        pygame.init()
        pygame.display.set_caption("Racing Game")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()  # Game start time

        # Create game objects
        self.road = Road(self.screen, self.window_height)
        self.dashboard = DashBoard(self.screen, self.clock, self.start_time, self.window_width)
        self.player = Player()
        self.obstacle = Obstacle(object_type="car")

        # Create sprites
        self.player_sprite = pygame.sprite.GroupSingle(self.player)
        self.obstacle_group = pygame.sprite.Group(self.obstacle)

        self.running = True

    def game_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if self.running:
                self.road.update()
                self.player_sprite.draw(self.screen)
                self.player.update()
                self.obstacle_group.draw(self.screen)
                self.obstacle.update(self.road.increase, self.road.acc)
                self.dashboard.update(self.road.speed, self.road.acc)

            pygame.display.flip()
            self.clock.tick(self.fps)

    def run(self):
        self.game_loop()


if __name__ == "__main__":
    Game().run()
