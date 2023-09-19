import math
import pygame


class Road:
    def __init__(self):
        self.image = pygame.image.load("img/road.png").convert()
        self.rect = self.image.get_rect(bottomleft=(0, 800))
        self.tiles = math.ceil(800 / self.image.get_height()) + 1
        self.scroll_speed = 0

    def animation_cycle(self):
        self.rect.y += 1

    def update(self):
        self.animation_cycle()


pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
running = True

pygame.display.set_caption("Endless Scrolling")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

road = Road()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    road.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()

