import pygame
from src.helpers import circular_waypoints, sine_wave_waypoints
from string import ascii_letters, digits

pygame.init()
FONT10 = pygame.font.Font('assets/font/visitorTT1BRK.ttf', 10)
FONT20 = pygame.font.Font('assets/font/visitor1.ttf', 20)

TITLE = 'Space Resistance'
VERSION = '1.5'

WIDTH, HEIGHT = 216, 250
SCALE = 4

OBJECT_SPEEDS = {
    'player': 120,
    'shot': 200,
    'boss': 40,
    'scroll': 30
}

COLORS = {
    'RED': [248, 0, 0],
    'YELLOW': [247, 201, 34],
    'WHITE': [255, 255, 255],
    'BLACK': [0, 0, 0],
    'GREY': [4, 4, 4],
    'GREEN': [0, 250, 0],
    'INDIGO': [80, 33, 173],
    'GOLD': [235, 147, 23]
}
ENEMY_WAVES = {
    # length in time: ~91s
    # length in pos = 2750
    0: {
        (100, 210): {
            'type': 'small_1',
            'quantity': 8,
            'delay': 500,
            'speed': 90,
            'waypoints': circular_waypoints(WIDTH, HEIGHT)
        },
        (400, 460): {
            'type': 'small_1',
            'quantity': 4,
            'delay': 500,
            'speed': 90,
            'waypoints': sine_wave_waypoints(WIDTH, HEIGHT)
        }

    }
}

ENEMY_DATA = {
    'small_1': {
        'frames': 'assets/img/enemy/small_1/',
        'energy': 10,
        'bump_power': 20,
        'shot_score': 6,
        'kill_score': 12,
        'can_shoot': True
    },
    'small_2': {
        'frames': 'assets/img/enemy/small_2/',
        'energy': 10,
        'bump_power': 20,
        'shot_score': 6,
        'kill_score': 12,
        'can_shoot': False    
    },
    'medium': {
        'frames': 'assets/img/enemy/medium/',
        'energy': 20,
        'bump_power': 40,
        'shot_score': 12,
        'kill_score': 24,
        'can_shoot': True
    },
    'large': {
        'frames': 'assets/img/enemy/large/',
        'energy': 30,
        'bump_power': 60,
        'shot_score': 24,
        'kill_score': 48,
        'can_shoot': True
    },
    'boss': {
        'frames': 'assets/img/boss/',
        'energy': 300,
        'bump_power': 60,
        'shot_score': 48,
        'kill_score': 5000,
        'can_shoot': True
    }
}

SOUND_EFFECTS = {
    'player_shot': {
        'channel': 5,
        'sound': pygame.mixer.Sound('assets/msx/fx/player_shot.ogg'),
        'vol': 0.6
    },
    'explosion': {
        'channel': 6,
        'sound': pygame.mixer.Sound('assets/msx/fx/explosion_2.ogg'),
        'vol': 1
    },
    'lost_life': {
        'channel': 7,
        'sound': pygame.mixer.Sound('assets/msx/fx/lost_life.ogg'),
        'vol': 1
    },
    'power_up': {
        'channel': 8,
        'sound': pygame.mixer.Sound('assets/msx/fx/power_up.ogg'),
        'vol': 1
    }
}

MUSIC_TRACKS = {
    'welcome_screen_music': {
        'channel': 0,
        'sound': pygame.mixer.Sound('assets/msx/music/Welcome_Screen.ogg'),
        'vol': 0.5
    },
    'levels_1_3_music': {
        'channel': 1,
        'sound': pygame.mixer.Sound('assets/msx/music/C64_Turrican_2.ogg'),
        'vol': 0.5
    },
    'level_4': {
        'channel': 2,
        'sound': pygame.mixer.Sound('assets/msx/music/C64_Turrican_2_boss.ogg'),
        'vol': 0.5
    },
    'game_over_screen': {
        'channel': 3,
        'sound': pygame.mixer.Sound('assets/msx/music/Congrats.ogg'),
        'vol': 0.7
    },
    'congrats_screen': {
        'channel': 4,
        'sound': pygame.mixer.Sound('assets/msx/music/Amiga_Lotus_2.ogg'),
        'vol': 1
    }
}


WELCOME_SCREEN_MESSAGES = [
    ('MADE BY PAICHIWO USING PYTHON / PYGAME', COLORS['WHITE'], 35),
    ('SPECIAL THANKS:', COLORS['YELLOW'], 45),
    ('DWIGHT - FOR YOUR GUIDANCE AND PATIENCE', COLORS['YELLOW'], 55),
    ('ANSIMUZ - FOR THIS BEAUTIFUL ASSETS', COLORS['YELLOW'], 65),
    ('PRESS [S] TO START', COLORS['RED'], 80)
]

ALLOWED_CHARACTERS = list(ascii_letters + digits)
