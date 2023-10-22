import pygame


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, powerup_type):
        super().__init__()

        self.powerup_type = powerup_type

        if self.powerup_type == "energy":
            self.energy_1 = pygame.image.load("assets/img/powerup/energy/energy_1.png").convert_alpha()
            self.energy_2 = pygame.image.load("assets/img/powerup/energy/energy_2.png").convert_alpha()
            self.energy_3 = pygame.image.load("assets/img/powerup/energy/energy_3.png").convert_alpha()
            self.energy_4 = pygame.image.load("assets/img/powerup/energy/energy_4.png").convert_alpha()
            self.energy_5 = pygame.image.load("assets/img/powerup/energy/energy_5.png").convert_alpha()
            self.energy_6 = pygame.image.load("assets/img/powerup/energy/energy_6.png").convert_alpha()
            self.powerup_frames = [self.energy_1, self.energy_2, self.energy_3, self.energy_4, self.energy_5, self.energy_6]
            self.powerup_index = 0
        
        self.image = self.powerup_frames[self.powerup_index]
        self.rect = self.image.get_rect(center=(-20, 50))
        
    def animate(self):
        self.powerup_index += 0.5
        if self.powerup_index >= len(self.powerup_frames):
            self.powerup_index = 0
        self.image = self.powerup_frames[int(self.powerup_index)]

    def movement(self):
        if self.powerup_type == "energy":
            self.rect.x += 1

    def action(self, player_energy, player_max_energy):
        if self.powerup_type == "energy":
            player_energy += 50
            if player_energy >= player_max_energy:
                player_energy = player_max_energy
            return player_energy

    def update(self):
        self.animate()
        self.movement()
