import pygame
import sys

WINDOW_SIZE = (500, 500)

class ExampleSprite(pygame.sprite.Sprite):
    def __init__(self, screen, group):
        super().__init__(group)

        self.screen = screen

        self.frames = [pygame.image.load('../assets/img/enemy/large/0.png').convert_alpha(),
                       pygame.image.load('../assets/img/enemy/large/1.png').convert_alpha()]
        self.frames_index = 0
        self.image = self.frames[self.frames_index]

        self.img_width, self.img_height = self.image.get_width(), self.image.get_height()
        self.original_img = pygame.transform.scale(self.image, (self.img_width * 4, self.img_height * 4))
        self.image = self.original_img
        self.rect = self.original_img.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))

        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)

        self.angle = 0
        self.rotation_speed = 50
        self.animation_speed = 10
        self.speed = 200


    def animate(self, dt):
        self.frames_index += self.animation_speed * dt
        if self.frames_index >= len(self.frames):
            self.frames_index = 0

        self.image = self.frames[int(self.frames_index)]
        self.original_img = pygame.transform.scale(self.image, (self.img_width * 4, self.img_height * 4))

    def rotate(self, dt):
        self.angle -= self.rotation_speed * dt
        rotated_img = pygame.transform.rotate(self.original_img, self.angle)
        self.rect = rotated_img.get_rect(center=self.rect.center)
        self.image = rotated_img

    def move(self, dt):
        keys = pygame.key.get_pressed()

        self.direction.y = -1 if keys[pygame.K_UP] else (1 if keys[pygame.K_DOWN] else 0)
        self.direction.x = -1 if keys[pygame.K_LEFT] else (1 if keys[pygame.K_RIGHT] else 0)

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.animate(dt)
        self.rotate(dt)
        self.move(dt)


class Game:
    def __init__(self):
        # Setup
        pygame.init()
        pygame.display.set_caption('Rotation Standard Setup')
        self.window_size = (500, 500)
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()

        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.example_sprite = ExampleSprite(self.screen, self.all_sprites)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.screen.fill('grey')

            self.all_sprites.draw(self.screen)
            self.all_sprites.update(dt)

            pygame.display.flip()


if __name__ == '__main__':
    Game().run()