import pygame
from src.Road import Road
from src.Player import Player


def fps_counter():
    """Display the current FPS rate"""
    fps = str(round(clock.get_fps(), 2))
    fps_text = FONT.render(f"FPS {fps}", 1, "Black")
    screen.blit(fps_text, (460, 750))


def show_time(start):
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time-start) // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer_text = "{:02}:{:02}".format(minutes, seconds)

    time_text = FONT.render(timer_text, 1, "Black")
    screen.blit(time_text, (460, 700))


pygame.init()
clock = pygame.time.Clock()

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
FONT = pygame.font.Font('font/joystix_mono.otf', 18)
running = True

start_time = pygame.time.get_ticks()

pygame.display.set_caption("Endless Scrolling")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SCALED, vsync=1)

road = Road(WINDOW_HEIGHT, FONT, screen)
player = pygame.sprite.GroupSingle(Player())

# MAIN GAME LOOP
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    road.update()
    player.draw(screen)
    player.update()

    fps_counter()
    show_time(start_time)

    pygame.display.update()
    clock.tick(60)

pygame.quit()
