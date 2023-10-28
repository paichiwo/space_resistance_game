import pygame


class WelcomeScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font("assets/font/visitor1.ttf", 10)

        self.anim_1 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_1.png").convert_alpha()
        self.anim_2 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_2.png").convert_alpha()
        self.anim_3 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_3.png").convert_alpha()
        self.anim_4 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_4.png").convert_alpha()
        self.anim_5 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_5.png").convert_alpha()
        self.anim_6 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_6.png").convert_alpha()
        self.anim_7 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_7.png").convert_alpha()
        self.anim_8 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_8.png").convert_alpha()
        self.anim_9 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_9.png").convert_alpha()
        self.anim_10 = pygame.image.load("assets/img/ui/welcome_screen/screen_anim_10.png").convert_alpha()
        self.screen_anim_frames = [self.anim_1, self.anim_2, self.anim_3, self.anim_4, self.anim_5,
                                   self.anim_6, self.anim_7, self.anim_8, self.anim_9, self.anim_10]
        self.screen_anim_index = 0

        self.anim_delay = 100
        self.last_anim_update = pygame.time.get_ticks()

    def show(self):

        cur = pygame.time.get_ticks()
        if cur - self.last_anim_update >= self.anim_delay:
            self.screen_anim_index = (self.screen_anim_index + 1) % len(self.screen_anim_frames)
            self.last_anim_update = cur

        self.screen.fill("black")

        anim_frame = self.screen_anim_frames[self.screen_anim_index]
        anim_rect = anim_frame.get_rect(topleft=(0, 0))
        self.screen.blit(anim_frame, anim_rect)

        message_text = self.font.render("PYTHON SHOOT'EM UP GAME", True, "white")
        start_text = self.font.render("Press 'S' to START", True, "white")

        message_rect = message_text.get_rect()
        start_rect = start_text.get_rect()

        message_rect.center = (self.screen_width // 2, self.screen_height // 2)
        start_rect.center = (self.screen_width // 2, self.screen_height // 2 + 10)

        self.screen.blit(message_text, message_rect)
        self.screen.blit(start_text, start_rect)
