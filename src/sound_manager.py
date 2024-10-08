import pygame


class SoundManager:
    """Manages all sounds for the game"""
    def __init__(self):
        pygame.mixer.init(44100, 16, 2, 4096)
        pygame.mixer.set_num_channels(16)

        self.channels = [pygame.mixer.Channel(i) for i in range(16)]
        self.master_volume = 0.5
        self.set_master_volume(self.master_volume)

    def play_music(self, music):
        self.clear_all_music_channels_except(music['channel'])
        self.play_track(channel=music['channel'], sound=music['sound'], volume=music['vol'])

    def clear_all_music_channels_except(self, channel):
        for i, ch in enumerate(self.channels[:5]):
            if i != channel:
                ch.stop()

    def play_sound(self, fx):
        self.play_sound_fx(channel=fx['channel'], sound=fx['sound'], volume=fx['vol'])

    def play_track(self, channel, sound, volume):
        if not self.channels[channel].get_busy():
            self.channels[channel].set_volume(volume)
            self.channels[channel].play(sound, loops=-1)

    def play_sound_fx(self, channel, sound, volume):
        if self.channels[channel].get_busy():
            self.channels[channel].stop()
        self.channels[channel].set_volume(self.master_volume * volume)
        self.channels[channel].play(sound)

    def stop_all_music(self):
        for channel in self.channels:
            channel.stop()

    def set_master_volume(self, volume):
        self.master_volume = max(0.0, min(volume, 1.0))
        for channel in self.channels:
            if channel.get_busy():
                sound = channel.get_sound()
                if sound:
                    channel.set_volume(self.master_volume * sound.get_volume())
