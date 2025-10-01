"""
Friends Application with Supabase Integration
"""

import pygame
from config import settings

class FriendsApp:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.name = "Friends"
        self.icon = "👥"
        
        self.font_small = pygame.font.Font(None, settings.FONTS['SMALL'])
        self.font_medium = pygame.font.Font(None, settings.FONTS['MEDIUM'])
        self.font_large = pygame.font.Font(None, settings.FONTS['LARGE'])
        
        self.friends = []
        self.selected = 0
        self.user_id = "demo_user"
        
        from services.supabase_service import SupabaseService
        self.supabase = SupabaseService()
        
        self.load_friends()
    
    def load_friends(self):
        if self.supabase.is_connected():
            self.friends = self.supabase.get_friends(self.user_id)
        else:
            self.friends = [
                {'id': '1', 'name': 'Player1', 'status': 'online', 'avatar': '👤'},
                {'id': '2', 'name': 'Player2', 'status': 'offline', 'avatar': '👤'},
                {'id': '3', 'name': 'Player3', 'status': 'online', 'avatar': '👤'},
            ]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = min(self.selected + 1, len(self.friends) - 1)
            elif event.key == pygame.K_UP:
                self.selected = max(self.selected - 1, 0)
            elif event.key == pygame.K_a or event.key == pygame.K_RETURN:
                if 0 <= self.selected < len(self.friends):
                    self.open_friend_profile(self.friends[self.selected])
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
        
        item_height = 40
        start_y = 40
        
        for i in range(len(self.friends)):
            y = start_y + i * item_height
            if touch_y >= y and touch_y < y + item_height:
                self.selected = i
                self.open_friend_profile(self.friends[i])
                break
    
    def open_friend_profile(self, friend):
        print(f"Opening profile for {friend.get('name', 'Unknown')}")
    
    def update(self, dt):
        pass
    
    def render(self, top_surface, bottom_surface):
        top_surface.fill(settings.COLORS['LIGHT'])
        
        title = self.font_large.render("👥 Friends", True, settings.COLORS['DARK'])
        top_surface.blit(title, (20, 20))
        
        if self.friends and 0 <= self.selected < len(self.friends):
            friend = self.friends[self.selected]
            
            profile_y = 100
            avatar = self.font_large.render(friend.get('avatar', '👤'), True, settings.COLORS['PRIMARY'])
            avatar_rect = avatar.get_rect(center=(top_surface.get_width() // 2, profile_y))
            top_surface.blit(avatar, avatar_rect)
            
            name = self.font_medium.render(friend.get('name', 'Unknown'), True, settings.COLORS['DARK'])
            name_rect = name.get_rect(center=(top_surface.get_width() // 2, profile_y + 60))
            top_surface.blit(name, name_rect)
            
            status = friend.get('status', 'offline')
            status_color = settings.COLORS['ONLINE_GREEN'] if status == 'online' else settings.COLORS['OFFLINE_GRAY']
            status_text = f"● {status.capitalize()}"
            status_surf = self.font_small.render(status_text, True, status_color)
            status_rect = status_surf.get_rect(center=(top_surface.get_width() // 2, profile_y + 90))
            top_surface.blit(status_surf, status_rect)
        
        bottom_surface.fill(settings.COLORS['SECONDARY'])
        
        list_title = self.font_small.render("Friend List:", True, settings.COLORS['DARK'])
        bottom_surface.blit(list_title, (10, 10))
        
        if not self.friends:
            no_friends = self.font_small.render("No friends yet", True, settings.COLORS['GRAY'])
            bottom_surface.blit(no_friends, (10, 40))
        else:
            item_height = 40
            start_y = 40
            
            for i, friend in enumerate(self.friends):
                y = start_y + i * item_height
                
                if i == self.selected:
                    pygame.draw.rect(bottom_surface, settings.COLORS['PRIMARY'], (5, y, bottom_surface.get_width() - 10, item_height - 2))
                
                status = friend.get('status', 'offline')
                status_color = settings.COLORS['ONLINE_GREEN'] if status == 'online' else settings.COLORS['OFFLINE_GRAY']
                
                pygame.draw.circle(bottom_surface, status_color, (20, y + 20), 5)
                
                name_text = friend.get('name', 'Unknown')
                color = settings.COLORS['WHITE'] if i == self.selected else settings.COLORS['DARK']
                name_surf = self.font_small.render(name_text, True, color)
                bottom_surface.blit(name_surf, (35, y + 12))
