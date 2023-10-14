import pygame


class Enemy(pygame.sprite.Sprite):

    def __init__(self, screen, bg_img_width, window_height):
        super().__init__()

        self.screen = screen
        self.bg_img_width = bg_img_width
        self.window_height = window_height

        self.paths = Paths()

        self.enemy_sm_1 = pygame.image.load("assets/img/enemy/enemy-small_a.png").convert_alpha()
        self.enemy_sm_2 = pygame.image.load("assets/img/enemy/enemy-small_b.png").convert_alpha()
        self.enemy_sm_frames = [self.enemy_sm_1, self.enemy_sm_2]
        self.enemy_sm_index = 0

        self.image = self.enemy_sm_frames[self.enemy_sm_index]
        self.rect = self.image.get_rect()

        self.speed = 1.2
        self.energy = 20

    def animate(self):
        self.enemy_sm_index += 0.5
        if self.enemy_sm_index >= len(self.enemy_sm_frames):
            self.enemy_sm_index = 0
        self.image = self.enemy_sm_frames[int(self.enemy_sm_index)]

    def movement(self):
        coordinates = self.paths.movement(self.paths.patterns["trapezoid_1"])
        self.rect.center = coordinates
        pygame.draw.lines(self.screen, "gray", True, self.paths.patterns["trapezoid_1"])

    def destroy(self):
        self.kill()

    def kill_off_screen(self):
        if self.rect.left > self.bg_img_width:
            self.kill()

    def update(self):
        self.animate()
        self.movement()
        self.kill_off_screen()


class Paths:
    def __init__(self):
        super().__init__()

        self.patterns = {
            "trapezoid_1": [(-10, 50), (250, 50), (250, 100), (100, 150)]
        }

        self.pattern_index = 0
        self.position = self.patterns["trapezoid_1"][self.pattern_index]
        self.speed = 1

    def movement(self, pattern):
        direction = pygame.math.Vector2(pattern[0]) - self.position
        if direction.length() <= self.speed:
            self.position = pattern[0]
            pattern.append(pattern[0])
            pattern.pop(0)
        else:
            direction.scale_to_length(self.speed)
            new_position = pygame.math.Vector2(self.position) + direction
            self.position = (new_position.x, new_position.y)
        return self.position
