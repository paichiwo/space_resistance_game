import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the window
window_size = (500, 500)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Basic Pygame Setup")

# Sprite
image = pygame.image.load('../assets/img/enemy/large/0.png').convert_alpha()
image = pygame.transform.scale(image, 2)
rect = image.get_rect()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with a color (optional)
    screen.fill((0, 0, 0))  # Black background

    screen.blit(image, rect)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()