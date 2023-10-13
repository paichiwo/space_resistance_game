import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, bg_img_width, window_height):
        super().__init__()

        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.enemy_sm_1 = pygame.image.load("assets/img/enemy/enemy-small_a.png").convert_alpha()
        self.enemy_sm_2 = pygame.image.load("assets/img/enemy/enemy-small_b.png").convert_alpha()
        self.enemy_sm_frames = [self.enemy_sm_1, self.enemy_sm_2]
        self.enemy_sm_index = 0

        self.image = self.enemy_sm_frames[self.enemy_sm_index]
        self.rect = self.image.get_rect(midbottom=(20, 100))

        self.speed = 1.2
        self.energy = 20

    def animate(self):
        self.enemy_sm_index += 0.5
        if self.enemy_sm_index >= len(self.enemy_sm_frames):
            self.enemy_sm_index = 0
        self.image = self.enemy_sm_frames[int(self.enemy_sm_index)]

    def movement(self):
        self.rect.x += self.speed

    def destroy(self):
        self.kill()

    def kill_off_screen(self):
        if self.rect.left > self.bg_img_width or self.rect.right < 0:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.kill_off_screen()
    