import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, enemy_pos):
        super().__init__()

        self.enemy_pos = enemy_pos

        explosion_1 = pygame.image.load("assets/img/explosion/explosion_a.png").convert_alpha()
        explosion_2 = pygame.image.load("assets/img/explosion/explosion_b.png").convert_alpha()
        explosion_3 = pygame.image.load("assets/img/explosion/explosion_c.png").convert_alpha()
        explosion_4 = pygame.image.load("assets/img/explosion/explosion_d.png").convert_alpha()
        explosion_5 = pygame.image.load("assets/img/explosion/explosion_e.png").convert_alpha()
        explosion_6 = pygame.image.load("assets/img/explosion/explosion_f.png").convert_alpha()

        self.explosion_frames = [explosion_1, explosion_2, explosion_3, explosion_4, explosion_5, explosion_6]
        self.explosion_index = 0
        self.animation_speed = 0.5

        self.image = self.explosion_frames[self.explosion_index]
        self.rect = self.image.get_rect(center=enemy_pos)

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
