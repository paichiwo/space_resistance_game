import sys
import pygame
import pygame._sdl2 as pg_sdl2
from src.player import Player, Fumes
from src.background import Background


class Game:

    def __init__(self):
        super().__init__()

        # Game constants
        self.window_width = 320
        self.window_height = 180
        self.scale = 4
        self.fps = 60
        self.running = True

        # Game setup
        pygame.init()
        pygame.display.set_caption("pyshump")
        self.screen = pygame.display.set_mode((self.window_width, self.window_height),
                                              flags=pygame.RESIZABLE | pygame.HIDDEN | pygame.SCALED,
                                              vsync=1)
        self.clock = pygame.time.Clock()

        # Scaled window setup
        self.window = pg_sdl2.Window.from_display_module()
        self.window.size = (self.window_width * self.scale, self.window_height * self.scale)
        self.window.position = pg_sdl2.WINDOWPOS_CENTERED
        self.window.show()

        # Create game objects
        self.bg = Background(self.screen, self.window_height)
        self.player = Player(self.bg.bg_1.get_width(), self.window_height)
        self.fume = Fumes()
        self.player_sprite = pygame.sprite.Group(self.fume, self.player)

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
        self.player_sprite.draw(self.screen)
        self.player.update()
        self.fume.update((self.player.rect.midbottom[0], self.player.rect.midbottom[1]+8))

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
