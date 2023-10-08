import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, bg_img_width, window_height, *args):
        super().__init__(*args)

        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.ship_mid_a = pygame.image.load("assets/img/ship/ship_middle_a.png").convert_alpha()
        self.ship_mid_b = pygame.image.load("assets/img/ship/ship_middle_b.png").convert_alpha()

        self.frames = [self.ship_mid_a, self.ship_mid_b]
        self.anim_index = 0

        self.image = None
        self.rect = None

        self.render()

    def render(self):
        self.image = self.frames[self.anim_index]
        self.rect = self.image.get_rect(midbottom=(self.bg_img_width / 2, self.window_height - 10))

    def animate(self):
        self.anim_index += 0.8
        if self.anim_index >= len(self.frames):
            self.anim_index = 0
        self.image = self.frames[int(self.anim_index)]

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= 2
        if keys[pygame.K_DOWN]:
            self.rect.y += 2
        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
        if keys[pygame.K_RIGHT]:
            self.rect.x += 2

    def update(self):
        self.animate()
        self.movement()
