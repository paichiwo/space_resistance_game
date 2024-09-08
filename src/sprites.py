from src.config import *
from src.helpers import import_assets


class Shot(pygame.sprite.Sprite):
    def __init__(self, rect, speed, group, shot_type='player', direction='up'):
        super().__init__(group)

        self.direction = direction
        self.frames = import_assets(f'assets/img/shot/{shot_type}/')
        self.index = 0
        self.animation_speed = 10
        self.speed = speed

        self.image = self.frames[0]
        self.rect = self.image.get_frect(midbottom=rect.midtop if shot_type == 'player' else rect.midbottom)

    def animate(self, dt):
        self.index += self.animation_speed * dt
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def movement(self, dt):
        if self.direction == 'up':
            self.rect.y -= self.speed * dt
        else:
            self.rect.x += self.direction[0] * self.speed * dt
            self.rect.y += self.direction[1] * self.speed * dt

    def kill_off_screen(self):
        if self.rect.bottom < 0:
            self.kill()

    def update(self, dt):
        self.animate(dt)
        self.movement(dt)
        self.kill_off_screen()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, group):
        super().__init__(group)

        self.position = position
        self.animation_speed = 20

        self.frames = import_assets('assets/img/explosion/')
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=self.position)

    def animate(self, dt):
        self.index += self.animation_speed * dt
        if self.index >= len(self.frames):
            self.index = 5
            self.kill()
        else:
            self.image = self.frames[int(self.index)]

    def update(self, dt):
        self.animate(dt)
