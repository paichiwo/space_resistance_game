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


class MessageBetweenLevels:
    def __init__(self, screen, text_array):
        self.screen = screen

        self.texts = [(FONT20.render(text_array[0], False, COLORS['WHITE']), (WIDTH // 2, HEIGHT // 2)),
                      (FONT10.render(text_array[1], False, COLORS['WHITE']), (WIDTH // 2, HEIGHT // 2 + 30))]

    def show(self):
        for text, pos in self.texts:
            self.screen.blit(text, text.get_rect(midtop=pos))

