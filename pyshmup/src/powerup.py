import pygame


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.energy_1 = pygame.image.load("assets/img/powerup/energy/energy_1.png").convert_alpha()
        self.energy_2 = pygame.image.load("assets/img/powerup/energy/energy_2.png").convert_alpha()
        self.energy_3 = pygame.image.load("assets/img/powerup/energy/energy_3.png").convert_alpha()
        self.energy_4 = pygame.image.load("assets/img/powerup/energy/energy_4.png").convert_alpha()
        self.energy_5 = pygame.image.load("assets/img/powerup/energy/energy_5.png").convert_alpha()
        self.energy_6 = pygame.image.load("assets/img/powerup/energy/energy_6.png").convert_alpha()
        
        self.energy_frames = [self.energy_1, self.energy_2, self.energy_3, self.energy_4, self.energy_5, self.energy_6]
        self.energy_index = 0
        
        self.image = self.energy_frames[self.energy_index]
        self.rect = self.image.get_rect(center=(0, 0))
        
    def animate(self):
        self.energy_index += 0.5
        if self.energy_index >= len(self.energy_frames):
            self.energy_index = 0
        self.image = self.energy_frames[int(self.energy_index)]

    def movement(self):
        self.rect.x += 1
    
    def update(self):
        self.animate()
        self.movement()
