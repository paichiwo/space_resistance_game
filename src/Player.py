import pygame


class Player(pygame.sprite.Sprite):
    """Creates a player object"""

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(midbottom=(300, 700))

    def movement(self):
        """Move the player's car left or right based on user input."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 3
            if self.rect.x <= 160:
                self.rect.x += 10
        if keys[pygame.K_RIGHT]:
            self.rect.x += 3
            if self.rect.x >= 390:
                self.rect.x -= 10

    def update(self):
        self.movement()
