import math
import pygame as py

class Road:
    def __init__(self, image_path, frame_width, frame_height, scroll_speed):
        self.bg = py.image.load(image_path).convert()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.scroll_speed = scroll_speed
        self.scroll = 0
        self.tiles = math.ceil(self.frame_height / self.bg.get_height()) + 1

    def update(self):
        self.scroll += self.scroll_speed  # Changed to subtract for opposite direction
        if self.scroll >= self.bg.get_height():
            self.scroll = 0

    def render(self, screen):
        for i in range(self.tiles):
            screen.blit(self.bg, (0, self.bg.get_height() * i + self.scroll))

def main():
    py.init()
    clock = py.time.Clock()

    FrameHeight = 800
    FrameWidth = 600

    # PYGAME FRAME WINDOW
    py.display.set_caption("Endless Scrolling in pygame")
    screen = py.display.set_mode((FrameWidth, FrameHeight))

    road = Road("img/road.png", FrameWidth, FrameHeight, 2)  # Adjust the scroll speed as needed

    # MAIN LOOP
    running = True
    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        road.render(screen)
        road.update()

        py.display.update()
        clock.tick(60)  # Adjust the frame rate as needed

    py.quit()

if __name__ == "__main__":
    main()
