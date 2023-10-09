import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, bg_img_width, window_height, *args):
        super().__init__(*args)

        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.ship_mid_a = pygame.image.load("assets/img/ship/ship_middle_a.png").convert_alpha()
        self.ship_mid_b = pygame.image.load("assets/img/ship/ship_middle_b.png").convert_alpha()

        self.ship_left_1_a = pygame.image.load("assets/img/ship/ship_left_1a.png").convert_alpha()
        self.ship_left_1_b = pygame.image.load("assets/img/ship/ship_left_1b.png").convert_alpha()
        self.ship_left_2_a = pygame.image.load("assets/img/ship/ship_left_2a.png").convert_alpha()
        self.ship_left_2_b = pygame.image.load("assets/img/ship/ship_left_2b.png").convert_alpha()

        self.ship_right_1_a = pygame.image.load("assets/img/ship/ship_right_1a.png").convert_alpha()
        self.ship_right_1_b = pygame.image.load("assets/img/ship/ship_right_1b.png").convert_alpha()
        self.ship_right_2_a = pygame.image.load("assets/img/ship/ship_right_2a.png").convert_alpha()
        self.ship_right_2_b = pygame.image.load("assets/img/ship/ship_right_2b.png").convert_alpha()

        self.frames_mid = [self.ship_mid_a, self.ship_mid_b]
        self.frames_mid_anim_index = 0

        self.frames_left_1 = [self.ship_left_1_a, self.ship_left_1_b]
        self.frames_left_1_anim_index = 0
        self.frames_left_2 = [self.ship_left_2_a, self.ship_left_2_b]
        self.frames_left_2_anim_index = 0

        self.frames_right_1 = [self.ship_right_1_a, self.ship_right_1_b]
        self.frames_right_1_anim_index = 0
        self.frames_right_2 = [self.ship_right_2_a, self.ship_right_2_b]
        self.frames_right_2_anim_index = 0

        self.image = None
        self.rect = None

        self.render()

    def render(self):
        """Render player image"""
        self.image = self.frames_mid[self.frames_mid_anim_index]
        self.rect = self.image.get_rect(midbottom=(self.bg_img_width / 2, self.window_height - 10))

    def animate_mid(self):
        self.frames_mid_anim_index += 0.8
        if self.frames_mid_anim_index >= len(self.frames_mid):
            self.frames_mid_anim_index = 0
        self.image = self.frames_mid[int(self.frames_mid_anim_index)]

    def animate_left(self):
        self.frames_left_1_anim_index += 0.8
        if self.frames_left_1_anim_index >= len(self.frames_left_1):
            self.frames_left_1_anim_index = 0
        self.image = self.frames_left_1[int(self.frames_left_1_anim_index)]

    def animate_right(self):
        self.frames_right_1_anim_index += 0.8
        if self.frames_right_1_anim_index >= len(self.frames_right_1):
            self.frames_right_1_anim_index = 0
        self.image = self.frames_right_1[int(self.frames_right_1_anim_index)]

    def movement(self):
        """Rules for moving the player"""

        self.animate_mid()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.rect.y -= 2

        if keys[pygame.K_DOWN]:
            self.rect.y += 2

        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
            self.animate_left()

        if keys[pygame.K_RIGHT]:
            self.rect.x += 2
            self.animate_right()

    def update(self):
        self.movement()
