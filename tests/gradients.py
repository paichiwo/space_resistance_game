import pygame

# Window size
WINDOW_WIDTH    = 400
WINDOW_HEIGHT   = 400

### initialisation
pygame.init()
window = pygame.display.set_mode( ( WINDOW_WIDTH, WINDOW_HEIGHT ) )
pygame.display.set_caption("Gradient Rect")

def gradientRect( window, left_colour, right_colour, target_rect ):
    """ Draw a horizontal-gradient filled rectangle covering <target_rect> """
    colour_rect = pygame.Surface( ( 2, 2 ) )                                   # tiny! 2x2 bitmap
    pygame.draw.line( colour_rect, left_colour,  ( 0,0 ), ( 0,1 ) )            # left colour line
    pygame.draw.line( colour_rect, right_colour, ( 1,0 ), ( 1,1 ) )            # right colour line
    colour_rect = pygame.transform.smoothscale( colour_rect, ( target_rect.width, target_rect.height ) )  # stretch!
    window.blit( colour_rect, target_rect )                                    # paint it


### Main Loop
clock = pygame.time.Clock()
finished = False
while not finished:

    # Handle user-input
    for event in pygame.event.get():
        if ( event.type == pygame.QUIT ):
            done = True

    # Update the window
    window.fill( ( 0,0,0 ) )
    gradientRect( window, (0, 255, 0), (0, 100, 0), pygame.Rect( 100,100, 100, 50 ) )
    gradientRect( window, (255, 255, 0), (0, 0, 255), pygame.Rect( 100,200, 128, 64 ) )
    pygame.display.flip()

    # Clamp FPS
    clock.tick_busy_loop(60)

pygame.quit()