import os

import pygame


class Explosion(pygame.sprite.Sprite):
    """Create explosion object"""
    def __init__(self, position):
        super().__init__()

        self.position = position

        # small explosion
        self.explosion_frames = []
        self.explosion_index = 0

        self.directory = "assets/img/explosion"
        for file in os.listdir(self.directory):
            if file.endswith(".png"):
                explosion_filename = os.path.join(self.directory, file)
                explosion_frame = pygame.image.load(explosion_filename).convert_alpha()
                self.explosion_frames.append(explosion_frame)

        self.animation_speed = 0.5

        self.image = self.explosion_frames[self.explosion_index]
        self.rect = self.image.get_rect(center=self.position)

    def animate(self):
        self.explosion_index += self.animation_speed
        if self.explosion_index >= len(self.explosion_frames):
            self.explosion_index = 5
            self.destroy()
        else:
            self.image = self.explosion_frames[int(self.explosion_index)]

    def destroy(self):
        self.kill()

    def update(self):
        self.animate()
