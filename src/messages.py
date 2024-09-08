from src.config import *
from src.timer import Timer


class Message:
    def __init__(self, screen, text, font, duration, pos):
        self.screen = screen
        self.text = text
        self.pos = pos

        self.outline = font.render(text, False, COLORS['BLACK'])
        self.text = font.render(text, False, COLORS['WHITE'])
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
            self.screen.blit(self.outline, (self.pos[0], self.pos[1]))
            self.screen.blit(self.text, (self.pos[0] + 1, self.pos[1] + 1))


class MessageBetweenLevels:
    def __init__(self, screen, text_array):
        self.screen = screen

        self.texts = [(FONT20.render(text_array[0], False, COLORS['WHITE']), (WIDTH // 2, HEIGHT // 2)),
                      (FONT10.render(text_array[1], False, COLORS['WHITE']), (WIDTH // 2, HEIGHT // 2 + 30))]

    def show(self):
        for text, pos in self.texts:
            self.screen.blit(text, text.get_rect(midtop=pos))
