import pygame


class SoundManager:
    """Manages all sounds for the game"""
    def __init__(self):

        # Initialize pygame mixer
        pygame.mixer.init(44100, 16, 2, 4096)
        pygame.mixer.set_num_channels(16)

        # Create channels
        self.channels = [pygame.mixer.Channel(i) for i in range(16)]

        # Load music tracks
        self.welcome_screen_music = pygame.mixer.Sound("assets/msx/music/Welcome_Screen.ogg")
        self.levels_1_3_music = pygame.mixer.Sound("assets/msx/music/C64_Turrican_2.ogg")
        self.level_4_music = pygame.mixer.Sound("assets/msx/music/C64_Turrican_2_boss.ogg")
        self.game_over_screen_music = pygame.mixer.Sound("assets/msx/music/Congrats.ogg")
        self.congrats_screen_music = pygame.mixer.Sound("assets/msx/music/Amiga_Lotus_2.ogg")

        # Set volume for music tracks
        self.welcome_screen_music.set_volume(0.5)
        self.levels_1_3_music.set_volume(0.5)
        self.level_4_music.set_volume(0.5)
        self.game_over_screen_music.set_volume(0.7)
        self.congrats_screen_music.set_volume(1)

        # Load sound effects
        self.player_shot_sound = pygame.mixer.Sound("assets/msx/fx/player_shot.ogg")
        self.explosion_sound = pygame.mixer.Sound("assets/msx/fx/explosion_2.ogg")
        self.lost_life_sound = pygame.mixer.Sound("assets/msx/fx/lost_life.ogg")
        self.power_up_sound = pygame.mixer.Sound("assets/msx/fx/power_up.ogg")

        # Set volume for sound effects
        self.player_shot_sound.set_volume(0.6)

    def play_welcome_screen_music(self):
        self.channels[1].stop()
        self.channels[2].stop()
        self.channels[3].stop()
        self.channels[4].stop()
        self.play_track(channel=0, sound=self.welcome_screen_music)

    def play_levels_1_3_music(self):
        self.channels[0].stop()
        self.channels[2].stop()
        self.channels[3].stop()
        self.channels[4].stop()
        self.play_track(channel=1, sound=self.levels_1_3_music)

    def play_level_4_music(self):
        self.channels[0].stop()
        self.channels[1].stop()
        self.channels[3].stop()
        self.channels[4].stop()
        self.play_track(channel=2, sound=self.level_4_music)

    def play_game_over_music(self):
        self.channels[0].stop()
        self.channels[1].stop()
        self.channels[2].stop()
        self.channels[4].stop()
        self.play_track(channel=3, sound=self.game_over_screen_music)

    def play_congrats_music(self):
        self.channels[0].stop()
        self.channels[1].stop()
        self.channels[2].stop()
        self.channels[3].stop()
        self.play_track(channel=4, sound=self.congrats_screen_music)

    def play_player_shot_fx(self):
        self.play_sound_fx(channel=5, sound=self.player_shot_sound)

    def play_explosion_fx(self):
        self.play_sound_fx(channel=6, sound=self.explosion_sound)

    def play_lost_life_fx(self):
        self.play_sound_fx(channel=7, sound=self.lost_life_sound)

    def play_power_up_fx(self):
        self.play_sound_fx(channel=8, sound=self.power_up_sound)

    def play_track(self, channel, sound):
        if not self.channels[channel].get_busy():
            self.channels[channel].play(sound, loops=-1)

    def play_sound_fx(self, channel, sound):
        if not self.channels[channel].get_busy():
            self.channels[channel].play(sound)

    def stop_all_music(self):
        for channel in self.channels:
            channel.stop()
