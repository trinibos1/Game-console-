"""
Web Browser Application with Touch Keyboard
"""

import pygame
from config import settings
from ui.widgets.keyboard import OnScreenKeyboard

class BrowserApp:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.name = "Browser"
        self.icon = "🌐"
        
        self.font_small = pygame.font.Font(None, settings.FONTS['SMALL'])
        self.font_medium = pygame.font.Font(None, settings.FONTS['MEDIUM'])
        self.font_large = pygame.font.Font(None, settings.FONTS['LARGE'])
        
        self.url = "https://www.example.com"
        self.bookmarks = [
            "https://www.google.com",
            "https://www.github.com",
            "https://www.raspberrypi.com"
        ]
        
        self.keyboard = OnScreenKeyboard(self.screen_manager.bottom_width, self.screen_manager.bottom_height)
        self.page_content = "Welcome to the browser!\n\nThis is a simple web browser.\nEnter a URL to browse."
    
    def handle_event(self, event):
        if self.keyboard.visible:
            window_width = self.screen_manager.window.get_width()
            bottom_x_offset = (window_width - self.screen_manager.bottom_width) // 2
            bottom_y_offset = self.screen_manager.top_height + 20
            
            if self.keyboard.handle_event(event, bottom_x_offset, bottom_y_offset):
                if not self.keyboard.visible:
                    self.url = self.keyboard.text
                    self.load_url(self.url)
                return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.keyboard.show(self.url, lambda text: self.load_url(text))
            elif event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
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
        
        url_bar = pygame.Rect(10, 10, 300, 25)
        if url_bar.collidepoint(touch_x, touch_y):
            self.keyboard.show(self.url, lambda text: self.load_url(text))
        
        bookmark_y = 50
        for i, bookmark in enumerate(self.bookmarks[:3]):
            bookmark_rect = pygame.Rect(10, bookmark_y + i * 30, 300, 25)
            if bookmark_rect.collidepoint(touch_x, touch_y):
                self.load_url(bookmark)
                break
    
    def load_url(self, url):
        self.url = url
        self.page_content = f"Loading: {url}\n\nContent would appear here.\n\nNote: Full browser rendering\nrequires additional libraries."
        print(f"Loading URL: {url}")
    
    def update(self, dt):
        pass
    
    def render(self, top_surface, bottom_surface):
        top_surface.fill(settings.COLORS['WHITE'])
        
        pygame.draw.rect(top_surface, settings.COLORS['SECONDARY'], (0, 0, top_surface.get_width(), 40))
        
        url_text = self.font_small.render(f"🌐 {self.url}", True, settings.COLORS['WHITE'])
        top_surface.blit(url_text, (10, 12))
        
        content_y = 60
        for line in self.page_content.split('\n'):
            line_surf = self.font_small.render(line, True, settings.COLORS['DARK'])
            top_surface.blit(line_surf, (20, content_y))
            content_y += 25
        
        bottom_surface.fill(settings.COLORS['SECONDARY'])
        
        if self.keyboard.visible:
            self.keyboard.render(bottom_surface)
        else:
            url_bar = pygame.Rect(10, 10, 300, 25)
            pygame.draw.rect(bottom_surface, settings.COLORS['WHITE'], url_bar)
            url_surf = self.font_small.render(self.url[:30], True, settings.COLORS['DARK'])
            bottom_surface.blit(url_surf, (15, 15))
            
            bookmarks_label = self.font_small.render("Bookmarks:", True, settings.COLORS['DARK'])
            bottom_surface.blit(bookmarks_label, (10, 40))
            
            bookmark_y = 50
            for i, bookmark in enumerate(self.bookmarks[:3]):
                bookmark_rect = pygame.Rect(10, bookmark_y + i * 30, 300, 25)
                pygame.draw.rect(bottom_surface, settings.COLORS['DARK'], bookmark_rect)
                
                bookmark_text = bookmark[:35]
                bookmark_surf = self.font_small.render(bookmark_text, True, settings.COLORS['WHITE'])
                bottom_surface.blit(bookmark_surf, (15, bookmark_y + i * 30 + 5))
