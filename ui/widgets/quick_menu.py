"""
Quick Menu Overlay with Brightness, Volume, and Bluetooth Controls
"""

import pygame
from config import settings

class QuickMenu:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.active = False
        self.brightness = settings.DISPLAY['DEFAULT_BRIGHTNESS']
        self.volume = settings.AUDIO['DEFAULT_VOLUME']
        
        self.font_small = pygame.font.Font(None, settings.FONTS['SMALL'])
        self.font_medium = pygame.font.Font(None, settings.FONTS['MEDIUM'])
        
        self.dragging_brightness = False
        self.dragging_volume = False
        
        self.bluetooth_devices = []
    
    def toggle(self):
        self.active = not self.active
    
    def is_active(self):
        return self.active
    
    def handle_event(self, event):
        if not self.active:
            return False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            return self.handle_touch_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging_brightness = False
            self.dragging_volume = False
        elif event.type == pygame.MOUSEMOTION and event.buttons[0]:
            return self.handle_touch_drag(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_b:
                self.active = False
                return True
        
        return True
    
    def handle_touch_down(self, pos):
        window_width = self.screen_manager.window.get_width()
        bottom_x_offset = (window_width - self.screen_manager.bottom_width) // 2
        bottom_y_offset = self.screen_manager.top_height + 20
        
        touch_x = pos[0] - bottom_x_offset
        touch_y = pos[1] - bottom_y_offset
        
        if touch_x < 0 or touch_x > self.screen_manager.bottom_width:
            return True
        if touch_y < 0 or touch_y > self.screen_manager.bottom_height:
            return True
        
        brightness_slider_rect = pygame.Rect(40, 60, 240, 20)
        volume_slider_rect = pygame.Rect(40, 110, 240, 20)
        
        if brightness_slider_rect.collidepoint(touch_x, touch_y):
            self.dragging_brightness = True
            self.update_brightness_from_pos(touch_x)
            return True
        
        if volume_slider_rect.collidepoint(touch_x, touch_y):
            self.dragging_volume = True
            self.update_volume_from_pos(touch_x)
            return True
        
        return True
    
    def handle_touch_drag(self, pos):
        if self.dragging_brightness or self.dragging_volume:
            window_width = self.screen_manager.window.get_width()
            bottom_x_offset = (window_width - self.screen_manager.bottom_width) // 2
            touch_x = pos[0] - bottom_x_offset
            
            if self.dragging_brightness:
                self.update_brightness_from_pos(touch_x)
            elif self.dragging_volume:
                self.update_volume_from_pos(touch_x)
            return True
        return False
    
    def update_brightness_from_pos(self, x):
        slider_x = 40
        slider_width = 240
        value = max(0, min(100, int((x - slider_x) / slider_width * 100)))
        self.brightness = value
    
    def update_volume_from_pos(self, x):
        slider_x = 40
        slider_width = 240
        value = max(0, min(100, int((x - slider_x) / slider_width * 100)))
        self.volume = value
        try:
            pygame.mixer.music.set_volume(value / 100.0)
        except:
            pass
    
    def render(self, surface):
        if not self.active:
            return
        
        overlay = pygame.Surface((surface.get_width(), surface.get_height()))
        overlay.set_alpha(240)
        overlay.fill(settings.COLORS['DARK'])
        surface.blit(overlay, (0, 0))
        
        title_surf = self.font_medium.render("Quick Menu", True, settings.COLORS['WHITE'])
        surface.blit(title_surf, (20, 20))
        
        brightness_label = self.font_small.render(f"Brightness: {self.brightness}%", True, settings.COLORS['WHITE'])
        surface.blit(brightness_label, (40, 45))
        
        slider_rect = pygame.Rect(40, 60, 240, 20)
        pygame.draw.rect(surface, settings.COLORS['SECONDARY'], slider_rect)
        fill_width = int(slider_rect.width * (self.brightness / 100))
        fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, fill_width, slider_rect.height)
        pygame.draw.rect(surface, settings.COLORS['PRIMARY'], fill_rect)
        pygame.draw.rect(surface, settings.COLORS['WHITE'], slider_rect, 2)
        
        volume_label = self.font_small.render(f"Volume: {self.volume}%", True, settings.COLORS['WHITE'])
        surface.blit(volume_label, (40, 95))
        
        slider_rect = pygame.Rect(40, 110, 240, 20)
        pygame.draw.rect(surface, settings.COLORS['SECONDARY'], slider_rect)
        fill_width = int(slider_rect.width * (self.volume / 100))
        fill_rect = pygame.Rect(slider_rect.x, slider_rect.y, fill_width, slider_rect.height)
        pygame.draw.rect(surface, settings.COLORS['SUCCESS'], fill_rect)
        pygame.draw.rect(surface, settings.COLORS['WHITE'], slider_rect, 2)
        
        bt_label = self.font_small.render("Bluetooth Devices:", True, settings.COLORS['WHITE'])
        surface.blit(bt_label, (40, 145))
        
        if not self.bluetooth_devices:
            no_devices = self.font_small.render("No devices connected", True, settings.COLORS['GRAY'])
            surface.blit(no_devices, (40, 165))
        
        close_text = self.font_small.render("Press B or ESC to close", True, settings.COLORS['GRAY'])
        surface.blit(close_text, (40, 210))
