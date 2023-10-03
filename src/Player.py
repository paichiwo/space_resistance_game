import pygame


class Player(pygame.sprite.Sprite):
    """Creates a player object"""

    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(midbottom=(300, 700))

        self.turn_speed = 3
        self.move_left = False
        self.move_right = False

    def movement(self):
        """Move the player's car left or right based on user input."""
        if self.move_left:
            self.rect.x += self.turn_speed
        if self.move_right:
            self.rect.x -= self.turn_speed

    def stay_on_road(self):
        if self.rect.x <= 160:
            self.rect.x += 10
        if self.rect.x >= 390:
            self.rect.x -= 10

    def update(self):
        self.movement()
        self.stay_on_road()
