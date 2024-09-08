import pygame
import sys
import pygame._sdl2 as sdl2

WIDTH, HEIGHT = 100, 100
SCALE = 4


class ExampleSprite(pygame.sprite.Sprite):
    def __init__(self, renderer, group):
        super().__init__(group)

        self.frames = [
            sdl2.Texture.from_surface(renderer, pygame.image.load("../assets/img/enemy/small_1/0.png")),
            sdl2.Texture.from_surface(renderer, pygame.image.load("../assets/img/enemy/small_1/1.png")),
        ]

        self.frames_index = 0
        self.image = self.frames[self.frames_index]
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

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

    def rotate(self, dt):
        self.angle -= self.rotation_speed * dt
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

    def move(self, dt):
        keys = pygame.key.get_pressed()

        self.direction.y = (
            -1 if keys[pygame.K_UP] else (1 if keys[pygame.K_DOWN] else 0)
        )
        self.direction.x = (
            -1 if keys[pygame.K_LEFT] else (1 if keys[pygame.K_RIGHT] else 0)
        )

        if self.direction.magnitude() > 0:
            self.direction.normalize_ip()

        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.animate(dt)
        self.rotate(dt)
        self.move(dt)

    def render(self):
        self.image.draw(dstrect=self.rect, angle=-self.angle)


class Game:
    def __init__(self):
        # Setup
        self.clock = pygame.time.Clock()
        self.window = pygame.Window(
            size=(WIDTH * SCALE, HEIGHT * SCALE), title="Clean Rotation Test"
        )
        self.renderer = sdl2.Renderer(self.window)
        self.renderer.logical_size = (WIDTH, HEIGHT)
        self.screen = pygame.Surface((WIDTH, HEIGHT))
        self.window.get_surface()

        self.all_sprites = pygame.sprite.Group()
        self.example_sprite = ExampleSprite(self.renderer, self.all_sprites)

    def run(self):
        while True:
            self.renderer.draw_color = "black"
            self.renderer.clear()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000

            self.all_sprites.update(dt)
            for sprite in self.all_sprites:
                sprite.render()

            self.renderer.present()


if __name__ == "__main__":
    Game().run()