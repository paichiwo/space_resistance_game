import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        explosion_1 = pygame.image.load("assets/img/explosion/explosion_a.png")
        explosion_2 = pygame.image.load("assets/img/explosion/explosion_b.png")
        explosion_3 = pygame.image.load("assets/img/explosion/explosion_c.png")
        explosion_4 = pygame.image.load("assets/img/explosion/explosion_d.png")
        explosion_5 = pygame.image.load("assets/img/explosion/explosion_e.png")
        explosion_6 = pygame.image.load("assets/img/explosion/explosion_f.png")

        self.explosion_frames = [explosion_1, explosion_2, explosion_3, explosion_4, explosion_5, explosion_6]
        self.explosion_index = 0

        self.image = self.explosion_frames[self.explosion_index]
        self.rect = self.image.get_rect()

    def animate(self):
        self.explosion_index += 0.5
        if self.explosion_index >= len(self.explosion_frames):
            self.explosion_index = 5
        self.image = self.explosion_frames[int(self.explosion_index)]

    def destroy(self):
        self.kill()

    def update(self):
        self.animate()
