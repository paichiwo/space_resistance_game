import pygame


class Player(pygame.sprite.Sprite):
    """Create the Player object"""
    def __init__(self, bg_img_width, window_height, *args):
        super().__init__(*args)

        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.ship_mid = pygame.image.load("assets/img/ship/middle.png").convert_alpha()

        self.ship_left_1 = pygame.image.load("assets/img/ship/left_1.png").convert_alpha()
        self.ship_left_2 = pygame.image.load("assets/img/ship/left_2.png").convert_alpha()
        self.left_frames = [self.ship_left_1, self.ship_left_2]
        self.left_index = 0

        self.ship_right_1 = pygame.image.load("assets/img/ship/right_1.png").convert_alpha()
        self.ship_right_2 = pygame.image.load("assets/img/ship/right_2.png").convert_alpha()
        self.right_frames = [self.ship_right_1, self.ship_right_2]
        self.right_index = 0

        self.image = None
        self.rect = None

        self.cur_energy = 100
        self.max_energy = 100

        self.shots = pygame.sprite.Group()
        self.shot_cooldown = 0
        self.shot_speed = 10
        self.shot_power = 10

        self.render()

    def render(self):
        """Render player image"""
        self.image = self.ship_mid
        self.rect = self.image.get_rect(midbottom=(self.bg_img_width / 2, self.window_height - 10))

    def animate_left(self):
        self.left_index += 0.5
        if self.left_index >= len(self.left_frames):
            self.left_index = 1
        self.image = self.left_frames[int(self.left_index)]

    def animate_right(self):
        self.right_index += 0.5
        if self.right_index >= len(self.right_frames):
            self.right_index = 1
        self.image = self.right_frames[int(self.right_index)]

    def movement(self):
        """Rules for moving the player"""
        self.image = self.ship_mid

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

    def action(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.shoot()

    def stay_within_boundaries(self):
        """Rules to stay on the screen"""
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.bg_img_width:
            self.rect.right = self.bg_img_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.window_height:
            self.rect.bottom = self.window_height

    def shoot(self):
        if self.shot_cooldown == 0:
            new_shot = Shot(self.rect)
            self.shots.add(new_shot)
            self.shot_cooldown = self.shot_speed

    def handle_shot_cooldown(self):
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1

    def get_damage(self):
        if self.cur_energy > 0:
            self.cur_energy -= 1
        if self.cur_energy <= 0:
            self.cur_energy = 0

    def update(self):
        self.movement()
        self.action()
        self.stay_within_boundaries()
        self.shots.update()
        self.handle_shot_cooldown()


class Fumes(pygame.sprite.Sprite):

    def __init__(self, *args):
        super().__init__(*args)

        self.fumes_1 = pygame.image.load("assets/img/ship/fumes_1.png")
        self.fumes_2 = pygame.image.load("assets/img/ship/fumes_2.png")
        self.fumes_frames = [self.fumes_1, self.fumes_2]
        self.fumes_index = 0

        self.image = None
        self.rect = None

        self.render()

    def render(self):
        """Render player image"""
        self.image = self.fumes_1
        self.rect = self.image.get_rect()

    def animate_fumes(self, player_pos):
        self.fumes_index += 0.5
        if self.fumes_index >= len(self.fumes_frames):
            self.fumes_index = 0
        self.image = self.fumes_frames[int(self.fumes_index)]
        self.rect.midbottom = player_pos

    def update(self, player_pos):
        self.animate_fumes(player_pos)


class Shot(pygame.sprite.Sprite):

    def __init__(self, player_rect):
        super().__init__()

        self.image = pygame.image.load("assets/img/shot/laser_a.png")
        self.rect = self.image.get_rect(midbottom=player_rect.midtop)

    def movement(self):
        self.rect.y -= 5

    def kill_off_screen(self):
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.movement()
        self.kill_off_screen()
