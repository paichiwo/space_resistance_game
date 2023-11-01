import pygame


class Boss(pygame.sprite.Sprite):
    def __init__(self, bg_img_width, window_height, *args):
        super().__init__(*args)

        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.boss_img_1 = pygame.image.load("assets/img/boss/boss_1.png").convert_alpha()
        self.boss_img_2 = pygame.image.load("assets/img/boss/boss_2.png").convert_alpha()
        self.boss_frames = [self.boss_img_1, self.boss_img_2]
        self.boss_index = 0

        self.image = self.boss_frames[self.boss_index]
        self.rect = self.image.get_rect(center=(self.bg_img_width, 10))

    def animate(self):
        self.boss_index += 0.5
        if self.boss_index >= len(self.boss_frames):
            self.boss_index = 0
        self.image = self.boss_frames[int(self.boss_index)]

    def update(self):
        self.animate()
