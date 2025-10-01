"""
Theme Manager for Custom Themes and Wallpapers
"""

import pygame
from config import settings
from pathlib import Path

class ThemeManager:
    def __init__(self):
        self.current_theme = 'default'
        self.themes = {
            'default': {
                'name': 'Default Blue',
                'primary': (52, 152, 219),
                'secondary': (149, 165, 166),
                'light': (236, 240, 241),
                'dark': (44, 62, 80),
            },
            'dark': {
                'name': 'Dark Mode',
                'primary': (41, 128, 185),
                'secondary': (52, 73, 94),
                'light': (52, 73, 94),
                'dark': (23, 32, 42),
            },
            'nintendo': {
                'name': 'Nintendo Red',
                'primary': (230, 0, 18),
                'secondary': (128, 128, 128),
                'light': (240, 240, 240),
                'dark': (64, 64, 64),
            },
            'forest': {
                'name': 'Forest Green',
                'primary': (39, 174, 96),
                'secondary': (149, 165, 166),
                'light': (236, 240, 241),
                'dark': (34, 153, 84),
            }
        }
        
        self.wallpaper = None
        self.wallpaper_path = settings.PATHS['ASSETS'] / 'wallpapers'
    
    def get_themes(self):
        return [(key, theme['name']) for key, theme in self.themes.items()]
    
    def set_theme(self, theme_id):
        if theme_id in self.themes:
            self.current_theme = theme_id
            theme = self.themes[theme_id]
            settings.COLORS['PRIMARY'] = theme['primary']
            settings.COLORS['SECONDARY'] = theme['secondary']
            settings.COLORS['LIGHT'] = theme['light']
            settings.COLORS['DARK'] = theme['dark']
            return True
        return False
    
    def get_current_theme(self):
        return self.current_theme
    
    def load_wallpaper(self, filename):
        try:
            wallpaper_file = self.wallpaper_path / filename
            if wallpaper_file.exists():
                self.wallpaper = pygame.image.load(str(wallpaper_file))
                return True
        except Exception as e:
            print(f"Error loading wallpaper: {e}")
        return False
    
    def get_wallpaper(self, size):
        if self.wallpaper:
            return pygame.transform.scale(self.wallpaper, size)
        return None
