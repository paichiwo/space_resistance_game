import pygame

pygame.init()
FONT10 = pygame.font.Font('assets/font/visitor1.ttf', 10)
FONT20 = pygame.font.Font('assets/font/visitor1.ttf', 20)

TITLE = 'Space Resistance'
VERSION = '0.5'

WIDTH, HEIGHT = 256, 180
SCALE = 4
BACKGROUND_WIDTH = 256

COLORS = {
    'RED': [248, 0, 0],
    'YELLOW': [247, 201, 34],
    'WHITE': [255, 255, 255],
    'BLACK': [0, 0, 0],
    'GREY': [4, 4, 4]
}

ENEMY_LEVEL_DATA = {
    '1': {
        'choices': [
            {'choice': 'small_1', 'probability': 2},
            {'choice': 'small_2', 'probability': 2},
            {'choice': 'medium', 'probability': 1}
        ],
        'speed': {'small_1': 90, 'small_2': 120, 'medium': 90},
        'spawning_intervals': [700, 1200]
    },
    '2': {
        'choices': [
            {'choice': 'small_1', 'probability': 2},
            {'choice': 'small_2', 'probability': 2},
            {'choice': 'medium', 'probability': 1},
            {'choice': 'large', 'probability': 1}
        ],
        'speed': {'small_1': 120, 'small_2': 90, 'medium': 90, 'large': 90},
        'spawning_intervals': [700, 1000]
    },
    '3': {
        'choices': [
            {'choice': 'small_1', 'probability': 1},
            {'choice': 'small_2', 'probability': 1},
            {'choice': 'medium', 'probability': 2},
            {'choice': 'large', 'probability': 2}
        ],
        'speed': {'small_1': 120, 'small_2': 120, 'medium': 90, 'large': 90},
        'spawning_intervals': [500, 1000]
    },
    '4': {
        'choices': [
            {'choice': 'small_1', 'probability': 1},
            {'choice': 'small_2', 'probability': 2}
        ],
        'speed': {'small_1': 1, 'small_2': 2},
        'spawning_intervals': [1000, 1500]
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
