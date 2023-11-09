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

        self.empty = pygame.image.load("assets/img/ship/empty.png")

        self.god_mode_mid_frames = [self.ship_mid, self.empty, self.ship_mid]
        self.god_mode_mid_index = 0

        self.god_mode_left_frames = [self.ship_left_1, self.empty, self.ship_left_2]
        self.god_mode_left_index = 0

        self.god_mode_right_frames = [self.ship_right_1, self.empty, self.ship_right_2]
        self.god_mode_right_index = 0

        self.image = self.ship_mid
        self.rect = self.image.get_rect(midbottom=(self.bg_img_width // 2, self.window_height - 10))

        self.cur_energy = 100
        self.max_energy = 100
        self.lives = 4

        self.shots = pygame.sprite.Group()
        self.shot_cooldown = 0
        self.shot_speed = 10
        self.shot_power = 10
        self.is_shooting = False

        # Sound Effects
        pygame.mixer.init(44100, 16, 8, 2048)
        self.channel = pygame.mixer.Channel(5)
        # player shot
        self.player_shot_sound = pygame.mixer.Sound("assets/msx/fx/player_shot.wav")
        self.player_shot_sound.set_volume(0.6)

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

    def animate_god_mode_mid(self):
        self.god_mode_mid_index += 0.5
        if self.god_mode_mid_index >= len(self.god_mode_mid_frames):
            self.god_mode_mid_index = 1
        self.image = self.god_mode_mid_frames[int(self.god_mode_mid_index)]

    def animate_god_mode_left(self):
        self.god_mode_left_index += 0.5
        if self.god_mode_left_index >= len(self.god_mode_left_frames):
            self.god_mode_left_index = 1
        self.image = self.god_mode_left_frames[int(self.god_mode_left_index)]

    def animate_god_mode_right(self):
        self.god_mode_right_index += 0.5
        if self.god_mode_right_index >= len(self.god_mode_right_frames):
            self.god_mode_right_index = 1
        self.image = self.god_mode_right_frames[int(self.god_mode_right_index)]

    def movement_animation_normal_mode(self, keys):
        self.image = self.ship_mid
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

    def movement_animation_god_mode(self, keys):
        self.animate_god_mode_mid()
        if keys[pygame.K_UP]:
            self.rect.y -= 2
        if keys[pygame.K_DOWN]:
            self.rect.y += 2
        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
            self.animate_god_mode_left()
        if keys[pygame.K_RIGHT]:
            self.rect.x += 2
            self.animate_god_mode_right()

    def movement(self, god_mode):
        """Rules for moving the player"""
        keys = pygame.key.get_pressed()
        if not god_mode:
            self.movement_animation_normal_mode(keys)
        else:
            self.movement_animation_god_mode(keys)

    def play_shot_sound(self):
        if not self.channel.get_busy():
            self.channel.play(self.player_shot_sound)

    def action(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.is_shooting:
            self.shoot()
            self.is_shooting = True
            self.play_shot_sound()

        elif not keys[pygame.K_SPACE]:
            self.is_shooting = False

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

    def get_damage(self, damage_value):
        if self.cur_energy > 0:
            self.cur_energy -= damage_value

    def update(self, god_mode):
        self.movement(god_mode)
        self.action()
        self.stay_within_boundaries()
        self.shots.update()
        self.handle_shot_cooldown()


class Fumes(pygame.sprite.Sprite):

    def __init__(self, *args):
        super().__init__(*args)

        self.fumes_1 = pygame.image.load("assets/img/ship/fumes_1.png").convert_alpha()
        self.fumes_2 = pygame.image.load("assets/img/ship/fumes_2.png").convert_alpha()
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

        self.laser_1 = pygame.image.load("assets/img/shot/laser_a.png").convert_alpha()
        self.laser_2 = pygame.image.load("assets/img/shot/laser_b.png").convert_alpha()
        self.laser_frames = [self.laser_1, self.laser_2]
        self.laser_index = 0

        self.image = self.laser_frames[self.laser_index]
        self.rect = self.image.get_rect(midbottom=player_rect.midtop)
        self.rect.x -= 1

    def animate(self):
        self.laser_index += 0.5
        if self.laser_index >= len(self.laser_frames):
            self.laser_index = 0
        self.image = self.laser_frames[int(self.laser_index)]

    def movement(self):
        self.rect.y -= 5

    def kill_off_screen(self):
        if self.rect.bottom < 0:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.kill_off_screen()
