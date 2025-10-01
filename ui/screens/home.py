"""
Home Screen with Status Bar and App Grid
"""

import pygame
from datetime import datetime
from config import settings

class HomeScreen:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.font_small = pygame.font.Font(None, settings.FONTS['SMALL'])
        self.font_medium = pygame.font.Font(None, settings.FONTS['MEDIUM'])
        self.font_large = pygame.font.Font(None, settings.FONTS['LARGE'])
        self.font_title = pygame.font.Font(None, settings.FONTS['TITLE'])
        
        self.selected_app = 0
        
        from services.app_registry import AppRegistry
        from ui.widgets.quick_menu import QuickMenu
        self.app_registry = AppRegistry()
        self.apps = self.app_registry.get_all_apps()
        self.quick_menu = QuickMenu(screen_manager)
        
        self.scroll_offset = 0
    
    def handle_event(self, event):
        if self.quick_menu.is_active():
            return self.quick_menu.handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_app = min(self.selected_app + 3, len(self.apps) - 1)
            elif event.key == pygame.K_UP:
                self.selected_app = max(self.selected_app - 3, 0)
            elif event.key == pygame.K_LEFT:
                self.selected_app = max(self.selected_app - 1, 0)
            elif event.key == pygame.K_RIGHT:
                self.selected_app = min(self.selected_app + 1, len(self.apps) - 1)
            elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                self.launch_selected_app()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_touch(event.pos)
    
    def handle_touch(self, pos):
        bottom_y_offset = self.screen_manager.top_height + 20
        touch_y = pos[1] - bottom_y_offset
        
        if touch_y < 0 or touch_y > self.screen_manager.bottom_height:
            return
        
        window_width = self.screen_manager.window.get_width()
        bottom_x_offset = (window_width - self.screen_manager.bottom_width) // 2
        touch_x = pos[0] - bottom_x_offset
        
        if touch_x < 0 or touch_x > self.screen_manager.bottom_width:
            return
        
        bar_height = 35
        if touch_y < bar_height:
            button_width = self.screen_manager.bottom_width // 4
            button_index = touch_x // button_width
            
            if button_index == 0:
                print("Friends quick access")
            elif button_index == 1:
                print("Notifications")
            elif button_index == 2:
                print("Browser quick access")
            elif button_index == 3:
                self.quick_menu.toggle()
            return
        
        grid_start_y = 40
        if touch_y > grid_start_y:
            grid_cols = 3
            cell_width = self.screen_manager.bottom_width // grid_cols
            cell_height = 80
            
            col = touch_x // cell_width
            row = (touch_y - grid_start_y) // cell_height
            index = row * grid_cols + col
            
            if index < len(self.apps):
                self.selected_app = index
                self.launch_selected_app()
    
    def launch_selected_app(self):
        if 0 <= self.selected_app < len(self.apps):
            app = self.apps[self.selected_app]
            print(f"Launching app: {app['name']}")
            
            app_class = self.app_registry.get_app(app['id'])
            if app_class:
                app_instance = app_class(self.screen_manager)
                self.screen_manager.push_screen(app_instance)
    
    def update(self, dt):
        pass
    
    def render(self, top_surface, bottom_surface):
        self.render_top_screen(top_surface)
        self.render_bottom_screen(bottom_surface)
    
    def render_top_screen(self, surface):
        surface.fill(settings.COLORS['LIGHT'])
        
        status_bar_height = 30
        pygame.draw.rect(surface, settings.COLORS['PRIMARY'], 
                        (0, 0, surface.get_width(), status_bar_height))
        
        now = datetime.now()
        time_text = now.strftime("%I:%M %p")
        time_surf = self.font_medium.render(time_text, True, settings.COLORS['WHITE'])
        surface.blit(time_surf, (10, 5))
        
        wifi_text = "📶"
        wifi_surf = self.font_medium.render(wifi_text, True, settings.COLORS['WHITE'])
        surface.blit(wifi_surf, (surface.get_width() - 80, 5))
        
        bt_text = "🔵"
        bt_surf = self.font_medium.render(bt_text, True, settings.COLORS['WHITE'])
        surface.blit(bt_surf, (surface.get_width() - 40, 5))
        
        if 0 <= self.selected_app < len(self.apps):
            app = self.apps[self.selected_app]
            preview_rect = pygame.Rect(100, 100, 600, 300)
            pygame.draw.rect(surface, settings.COLORS['WHITE'], preview_rect)
            pygame.draw.rect(surface, settings.COLORS['PRIMARY'], preview_rect, 3)
            
            icon_surf = self.font_title.render(app['icon'], True, settings.COLORS['PRIMARY'])
            icon_rect = icon_surf.get_rect(center=(preview_rect.centerx, preview_rect.centery - 40))
            surface.blit(icon_surf, icon_rect)
            
            name_surf = self.font_large.render(app['name'], True, settings.COLORS['DARK'])
            name_rect = name_surf.get_rect(center=(preview_rect.centerx, preview_rect.centery + 40))
            surface.blit(name_surf, name_rect)
    
    def render_bottom_screen(self, surface):
        surface.fill(settings.COLORS['SECONDARY'])
        
        if self.quick_menu.is_active():
            self.quick_menu.render(surface)
            return
        
        bar_height = 35
        pygame.draw.rect(surface, settings.COLORS['DARK'], 
                        (0, 0, surface.get_width(), bar_height))
        
        button_width = surface.get_width() // 4
        buttons = ['👥', '🔔', '🌐', '☰']
        for i, icon in enumerate(buttons):
            text_surf = self.font_medium.render(icon, True, settings.COLORS['WHITE'])
            text_rect = text_surf.get_rect(center=(button_width * i + button_width // 2, bar_height // 2))
            surface.blit(text_surf, text_rect)
        
        grid_start_y = bar_height + 5
        grid_cols = 3
        cell_width = surface.get_width() // grid_cols
        cell_height = 80
        
        for i, app in enumerate(self.apps):
            row = i // grid_cols
            col = i % grid_cols
            
            x = col * cell_width
            y = grid_start_y + row * cell_height
            
            if i == self.selected_app:
                pygame.draw.rect(surface, settings.COLORS['PRIMARY'], 
                               (x + 2, y + 2, cell_width - 4, cell_height - 4), 3)
            
            icon_surf = self.font_large.render(app['icon'], True, settings.COLORS['DARK'])
            icon_rect = icon_surf.get_rect(center=(x + cell_width // 2, y + cell_height // 2 - 15))
            surface.blit(icon_surf, icon_rect)
            
            name_surf = self.font_small.render(app['name'], True, settings.COLORS['DARK'])
            name_rect = name_surf.get_rect(center=(x + cell_width // 2, y + cell_height // 2 + 20))
            surface.blit(name_surf, name_rect)
