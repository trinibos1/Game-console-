"""
Dual Screen Manager for Top and Bottom Screens
"""

import pygame
from config import settings

class ScreenManager:
    def __init__(self):
        self.top_width = settings.DISPLAY['TOP_WIDTH']
        self.top_height = settings.DISPLAY['TOP_HEIGHT']
        self.bottom_width = settings.DISPLAY['BOTTOM_WIDTH']
        self.bottom_height = settings.DISPLAY['BOTTOM_HEIGHT']
        
        window_width = max(self.top_width, self.bottom_width)
        window_height = self.top_height + self.bottom_height + 20
        
        self.window = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Gaming System")
        
        self.top_surface = pygame.Surface((self.top_width, self.top_height))
        self.bottom_surface = pygame.Surface((self.bottom_width, self.bottom_height))
        
        from ui.screens.home import HomeScreen
        self.current_screen = HomeScreen(self)
        self.screen_stack = []
    
    def go_home(self):
        from ui.screens.home import HomeScreen
        self.screen_stack.clear()
        self.current_screen = HomeScreen(self)
    
    def push_screen(self, screen):
        if self.current_screen:
            self.screen_stack.append(self.current_screen)
        self.current_screen = screen
    
    def pop_screen(self):
        if self.screen_stack:
            self.current_screen = self.screen_stack.pop()
            return True
        return False
    
    def handle_event(self, event):
        if self.current_screen:
            self.current_screen.handle_event(event)
    
    def update(self, dt):
        if self.current_screen:
            self.current_screen.update(dt)
    
    def render(self):
        self.window.fill(settings.COLORS['BLACK'])
        
        if self.current_screen:
            self.current_screen.render(self.top_surface, self.bottom_surface)
        
        top_x = (self.window.get_width() - self.top_width) // 2
        self.window.blit(self.top_surface, (top_x, 0))
        
        bottom_x = (self.window.get_width() - self.bottom_width) // 2
        bottom_y = self.top_height + 20
        self.window.blit(self.bottom_surface, (bottom_x, bottom_y))
        
        pygame.draw.rect(self.window, settings.COLORS['DARK'], 
                        (0, self.top_height, self.window.get_width(), 20))
