"""
Comprehensive Settings Application
"""

import pygame
from config import settings

class SettingsApp:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.name = "Settings"
        self.icon = "⚙️"
        
        self.font_small = pygame.font.Font(None, settings.FONTS['SMALL'])
        self.font_medium = pygame.font.Font(None, settings.FONTS['MEDIUM'])
        self.font_large = pygame.font.Font(None, settings.FONTS['LARGE'])
        
        self.sections = [
            {'id': 'profile', 'name': 'User Profile', 'icon': '👤'},
            {'id': 'wifi', 'name': 'WiFi', 'icon': '📶'},
            {'id': 'bluetooth', 'name': 'Bluetooth', 'icon': '🔵'},
            {'id': 'display', 'name': 'Display', 'icon': '🖥️'},
            {'id': 'audio', 'name': 'Audio', 'icon': '🔊'},
            {'id': 'network', 'name': 'Network', 'icon': '🌐'},
            {'id': 'themes', 'name': 'Themes', 'icon': '🎨'},
            {'id': 'controls', 'name': 'Controls', 'icon': '🎮'},
            {'id': 'storage', 'name': 'Storage', 'icon': '💾'},
            {'id': 'system', 'name': 'System', 'icon': '⚙️'},
            {'id': 'privacy', 'name': 'Privacy', 'icon': '🔒'},
            {'id': 'about', 'name': 'About', 'icon': 'ℹ️'},
        ]
        
        self.selected = 0
        self.current_section = None
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = min(self.selected + 1, len(self.sections) - 1)
            elif event.key == pygame.K_UP:
                self.selected = max(self.selected - 1, 0)
            elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                self.open_section(self.sections[self.selected]['id'])
            elif event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                if self.current_section:
                    self.current_section = None
                else:
                    self.screen_manager.pop_screen()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_touch(event.pos)
        
        return True
    
    def handle_touch(self, pos):
        window_width = self.screen_manager.window.get_width()
        bottom_x_offset = (window_width - self.screen_manager.bottom_width) // 2
        bottom_y_offset = self.screen_manager.top_height + 20
        
        touch_x = pos[0] - bottom_x_offset
        touch_y = pos[1] - bottom_y_offset
        
        if touch_x < 0 or touch_x > self.screen_manager.bottom_width:
            return
        if touch_y < 0 or touch_y > self.screen_manager.bottom_height:
            return
        
        item_height = 30
        start_y = 10
        
        for i, section in enumerate(self.sections):
            y = start_y + i * item_height
            if touch_y >= y and touch_y < y + item_height:
                self.selected = i
                self.open_section(section['id'])
                break
    
    def open_section(self, section_id):
        self.current_section = section_id
        print(f"Opening settings section: {section_id}")
    
    def update(self, dt):
        pass
    
    def render(self, top_surface, bottom_surface):
        top_surface.fill(settings.COLORS['LIGHT'])
        
        title = self.font_large.render("Settings", True, settings.COLORS['DARK'])
        top_surface.blit(title, (20, 20))
        
        if self.current_section:
            section = next((s for s in self.sections if s['id'] == self.current_section), None)
            if section:
                section_title = self.font_medium.render(f"{section['icon']} {section['name']}", True, settings.COLORS['DARK'])
                top_surface.blit(section_title, (20, 70))
                
                content_text = self.font_small.render(f"Configure {section['name'].lower()} settings here", True, settings.COLORS['GRAY'])
                top_surface.blit(content_text, (20, 110))
        else:
            if 0 <= self.selected < len(self.sections):
                section = self.sections[self.selected]
                preview_title = self.font_medium.render(f"{section['icon']} {section['name']}", True, settings.COLORS['PRIMARY'])
                top_surface.blit(preview_title, (20, 70))
        
        bottom_surface.fill(settings.COLORS['SECONDARY'])
        
        item_height = 30
        start_y = 10
        
        for i, section in enumerate(self.sections):
            y = start_y + i * item_height
            
            if i == self.selected:
                pygame.draw.rect(bottom_surface, settings.COLORS['PRIMARY'], (5, y, bottom_surface.get_width() - 10, item_height - 2))
            
            text = f"{section['icon']} {section['name']}"
            color = settings.COLORS['WHITE'] if i == self.selected else settings.COLORS['DARK']
            text_surf = self.font_small.render(text, True, color)
            bottom_surface.blit(text_surf, (15, y + 8))
