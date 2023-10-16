import pygame


class GameOverScreen:
    def __init__(self, screen_width, screen_height, screen):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = screen
        self.font = pygame.font.Font(None, 30)

    def show(self):

        self.screen.fill("black")

        game_over_text = self.font.render("Game Over", True, "red")
        restart_text = self.font.render("Press 'S' to START", True, "white")

        game_over_rect = game_over_text.get_rect()
        restart_rect = restart_text.get_rect()

        game_over_rect.center = (self.screen_width // 2, self.screen_height // 2 - 50)
        restart_rect.center = (self.screen_width // 2, self.screen_height // 2 + 50)

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
