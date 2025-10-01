"""
On-Screen Touch Keyboard Widget
"""

import pygame
from config import settings

class OnScreenKeyboard:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.visible = False
        self.text = ""
        self.callback = None
        
        self.font = pygame.font.Font(None, 18)
        
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', '⌫'],
            ['@', '.', 'space', '✓']
        ]
        
        self.shift = False
    
    def show(self, initial_text="", callback=None):
        self.visible = True
        self.text = initial_text
        self.callback = callback
    
    def hide(self):
        self.visible = False
        if self.callback:
            self.callback(self.text)
    
    def handle_event(self, event, offset_x=0, offset_y=0):
        if not self.visible:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            touch_x = event.pos[0] - offset_x
            touch_y = event.pos[1] - offset_y
            
            key_height = 28
            key_start_y = self.height - len(self.keys) * key_height - 5
            
            if touch_y < key_start_y:
                return True
            
            row_index = int((touch_y - key_start_y) / key_height)
            if row_index < 0 or row_index >= len(self.keys):
                return True
            
            row = self.keys[row_index]
            key_width = self.width // len(row)
            key_index = int(touch_x / key_width)
            
            if key_index >= 0 and key_index < len(row):
                key = row[key_index]
                self.handle_key(key)
            
            return True
        
        return False
    
    def handle_key(self, key):
        if key == '⌫':
            self.text = self.text[:-1]
        elif key == 'space':
            self.text += ' '
        elif key == '✓':
            self.hide()
        else:
            if self.shift:
                key = key.upper()
            self.text += key
    
    def render(self, surface):
        if not self.visible:
            return
        
        bg_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(surface, settings.COLORS['DARK'], bg_rect)
        
        text_surf = self.font.render(self.text + "|", True, settings.COLORS['WHITE'])
        surface.blit(text_surf, (10, 10))
        
        key_height = 28
        key_start_y = self.height - len(self.keys) * key_height - 5
        
        for row_idx, row in enumerate(self.keys):
            key_width = self.width // len(row)
            y = key_start_y + row_idx * key_height
            
            for key_idx, key in enumerate(row):
                x = key_idx * key_width
                
                key_rect = pygame.Rect(x + 2, y + 2, key_width - 4, key_height - 4)
                pygame.draw.rect(surface, settings.COLORS['SECONDARY'], key_rect)
                pygame.draw.rect(surface, settings.COLORS['WHITE'], key_rect, 1)
                
                key_text = 'space' if key == 'space' else key
                text_surf = self.font.render(key_text, True, settings.COLORS['WHITE'])
                text_rect = text_surf.get_rect(center=key_rect.center)
                surface.blit(text_surf, text_rect)
