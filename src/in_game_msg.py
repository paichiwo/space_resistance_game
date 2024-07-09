from src.config import *
from src.timer import Timer


class Message:
    def __init__(self, screen, text, duration):
        self.screen = screen
        self.text = text

        self.outline = FONT20.render(text, False, COLORS['BLACK'])
        self.text = FONT20.render(text, False, COLORS['WHITE'])
        self.timer = Timer(duration, self.hide)
        self.visible = False

    def show(self):
        self.visible = True
        self.timer.activate()

    def hide(self):
        self.visible = False

    def update(self):
        self.timer.update()
        if self.visible:
            self.screen.blit(self.outline, (BACKGROUND_WIDTH // 2 - 54, HEIGHT // 2 - 19))
            self.screen.blit(self.text, (BACKGROUND_WIDTH // 2 - 55, HEIGHT // 2 - 20))
