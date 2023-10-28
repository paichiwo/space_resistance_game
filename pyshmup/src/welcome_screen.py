import pygame


class WelcomeScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font("assets/font/visitor1.ttf", 10)

    def show(self):

        self.screen.fill("black")

        message_text = self.font.render("PYTHON SHOOT'EM UP GAME", True, "white")
        start_text = self.font.render("Press 'S' to START", True, "white")

        message_rect = message_text.get_rect()
        start_rect = start_text.get_rect()

        message_rect.center = (self.screen_width // 2, self.screen_height // 2)
        start_rect.center = (self.screen_width // 2, self.screen_height // 2 + 10)

        self.screen.blit(message_text, message_rect)
        self.screen.blit(start_text, start_rect)
