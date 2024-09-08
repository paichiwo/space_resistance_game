import sys
import pygame

pygame.init()
WIDTH, HEIGHT = 640, 480


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Joystick Example')
        self.clock = pygame.time.Clock()

        self.joysticks = {}
        self.player_surf = pygame.surface.Surface((40, 40))
        self.player_rect = self.player_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.player_surf.fill('blue')

    def add_joystick(self, device_index):
        joy = pygame.joystick.Joystick(device_index)
        self.joysticks[joy.get_instance_id()] = joy
        print(f'Joystick {joy.get_instance_id(), joy.get_name()} connected')

    def remove_joystick(self, instance_id):
        if instance_id in self.joysticks:
            del self.joysticks[instance_id]
            print(f'Joystick {instance_id} disconnected')

    def button_action(self, color):
        self.player_surf.fill(color)

    def handle_buttons(self, button):
        button_mapping = {
            0: 'green',
            1: 'red',
            2: 'blue',
            3: 'yellow'
        }
        if button in button_mapping:
            self.button_action(button_mapping[button])

    def draw_player(self):
        self.screen.blit(self.player_surf, self.player_rect)

    def input(self):
        for joy in self.joysticks.values():
            axes = joy.get_numaxes()

            if axes > 0:
                x_axis = joy.get_axis(0)
                y_axis = joy.get_axis(1)
                self.player_rect.x += int(x_axis * 5)
                self.player_rect.y += int(y_axis * 5)

    def run(self):
        while True:
            self.screen.fill('black')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.JOYBUTTONDOWN:
                    self.handle_buttons(event.button)
                elif event.type == pygame.JOYDEVICEADDED:
                    self.add_joystick(event.device_index)
                elif event.type == pygame.JOYDEVICEREMOVED:
                    self.remove_joystick(event.instance_id)

            self.draw_player()
            self.input()

            self.clock.tick(60)
            pygame.display.flip()
            print(self.joysticks)


if __name__ == '__main__':
    Game().run()
