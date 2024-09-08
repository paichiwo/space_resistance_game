import sys
import pygame


class Game:
    def __init__(self):

        pygame.init()
        pygame.mixer.init()

        mod_file = 'c:/Users/lzeru/Downloads/Lotus 2/modbootup.mod'
        xm_file = '../assets/msx/music/mods/lotuscr1.xm'

        try:
            pygame.mixer.music.load(mod_file)
            pygame.mixer.music.play(loops=-1, start=6)
            print(f'playing {mod_file}... press CTRL+C to stop.')

        except pygame.error as e:
            print(e)
            sys.exit()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

if __name__ == '__main__':
    Game()