"""
System Settings Configuration
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

DISPLAY = {
    'TOP_WIDTH': 800,
    'TOP_HEIGHT': 480,
    'BOTTOM_WIDTH': 320,
    'BOTTOM_HEIGHT': 240,
    'FPS': 60,
    'DEFAULT_BRIGHTNESS': 80,
}

COLORS = {
    'PRIMARY': (52, 152, 219),
    'SECONDARY': (149, 165, 166),
    'SUCCESS': (46, 204, 113),
    'DANGER': (231, 76, 60),
    'WARNING': (241, 196, 15),
    'LIGHT': (236, 240, 241),
    'DARK': (44, 62, 80),
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),
    'GRAY': (127, 140, 141),
    'ONLINE_GREEN': (46, 204, 113),
    'OFFLINE_GRAY': (149, 165, 166),
}

FONTS = {
    'SMALL': 12,
    'MEDIUM': 16,
    'LARGE': 20,
    'TITLE': 24,
    'STATUS_BAR': 14,
}

ANIMATION = {
    'TRANSITION_SPEED': 0.2,
    'FADE_SPEED': 0.15,
    'SLIDE_SPEED': 0.25,
}

PATHS = {
    'GAMES': BASE_DIR / 'games',
    'THEMES': BASE_DIR / 'themes',
    'ASSETS': BASE_DIR / 'assets',
    'DATA': BASE_DIR / 'data',
    'PLAYLISTS': BASE_DIR / 'data' / 'playlists',
    'SAVES': BASE_DIR / 'data' / 'saves',
}

AUDIO = {
    'DEFAULT_VOLUME': 70,
    'MUSIC_FORMATS': ['.mp3', '.ogg', '.wav', '.flac'],
    'SOUND_EFFECTS': True,
}

NETWORK = {
    'SUPABASE_URL': os.getenv('SUPABASE_URL', ''),
    'SUPABASE_KEY': os.getenv('SUPABASE_KEY', ''),
    'AUTO_CONNECT': True,
}

SYSTEM = {
    'AUTO_START_MUSIC': False,
    'PERFORMANCE_MODE': 'balanced',
    'SCREEN_TIMEOUT': 300,
    'LANGUAGE': 'en',
    'AUTO_UPDATE': True,
    'UPDATE_CHECK_INTERVAL': 3600,
    'UPDATE_REPO_URL': os.getenv('UPDATE_REPO_URL', ''),
}
