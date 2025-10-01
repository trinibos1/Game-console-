"""
Chat Application with Real-Time Messaging via Supabase
"""

import pygame
from config import settings
from ui.widgets.keyboard import OnScreenKeyboard

class ChatApp:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.name = "Chat"
        self.icon = "💬"
        
        self.font_small = pygame.font.Font(None, settings.FONTS['SMALL'])
        self.font_medium = pygame.font.Font(None, settings.FONTS['MEDIUM'])
        self.font_large = pygame.font.Font(None, settings.FONTS['LARGE'])
        
        self.messages = []
        self.current_message = ""
        self.user_id = "demo_user"
        self.friend_id = None
        
        self.keyboard = OnScreenKeyboard(self.screen_manager.bottom_width, self.screen_manager.bottom_height)
        
        from services.supabase_service import SupabaseService
        self.supabase = SupabaseService()
        
        self.load_demo_messages()
    
    def load_demo_messages(self):
        self.messages = [
            {'sender': 'friend', 'message': 'Hey! How are you?', 'time': '10:30'},
            {'sender': 'me', 'message': 'Good! Just playing some games.', 'time': '10:31'},
            {'sender': 'friend', 'message': 'Nice! Want to play together?', 'time': '10:32'},
        ]
    
    def handle_event(self, event):
        if self.keyboard.visible:
            window_width = self.screen_manager.window.get_width()
            bottom_x_offset = (window_width - self.screen_manager.bottom_width) // 2
            bottom_y_offset = self.screen_manager.top_height + 20
            
            if self.keyboard.handle_event(event, bottom_x_offset, bottom_y_offset):
                if not self.keyboard.visible:
                    self.current_message = self.keyboard.text
                    if self.current_message:
                        self.send_message(self.current_message)
                        self.current_message = ""
                return True
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.keyboard.show("", lambda text: self.send_message(text))
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
        
        send_btn = pygame.Rect(200, 200, 100, 30)
        if send_btn.collidepoint(touch_x, touch_y):
            self.keyboard.show("", lambda text: self.send_message(text))
    
    def send_message(self, message):
        if not message:
            return
        
        self.messages.append({
            'sender': 'me',
            'message': message,
            'time': '10:35'
        })
        
        if self.supabase.is_connected() and self.friend_id:
            self.supabase.send_message(self.user_id, self.friend_id, message)
    
    def update(self, dt):
        pass
    
    def render(self, top_surface, bottom_surface):
        top_surface.fill(settings.COLORS['LIGHT'])
        
        title = self.font_medium.render("💬 Chat", True, settings.COLORS['DARK'])
        top_surface.blit(title, (20, 20))
        
        message_start_y = 60
        message_height = 35
        
        for i, msg in enumerate(self.messages[-8:]):
            y = message_start_y + i * message_height
            
            is_me = msg['sender'] == 'me'
            x = 400 if is_me else 20
            
            bubble_color = settings.COLORS['PRIMARY'] if is_me else settings.COLORS['SECONDARY']
            bubble_rect = pygame.Rect(x, y, 350, 30)
            pygame.draw.rect(top_surface, bubble_color, bubble_rect, border_radius=10)
            
            text_color = settings.COLORS['WHITE'] if is_me else settings.COLORS['DARK']
            msg_surf = self.font_small.render(msg['message'][:40], True, text_color)
            top_surface.blit(msg_surf, (x + 10, y + 8))
        
        bottom_surface.fill(settings.COLORS['DARK'])
        
        if self.keyboard.visible:
            self.keyboard.render(bottom_surface)
        else:
            input_label = self.font_small.render("Tap to type message:", True, settings.COLORS['WHITE'])
            bottom_surface.blit(input_label, (10, 180))
            
            send_btn = pygame.Rect(200, 200, 100, 30)
            pygame.draw.rect(bottom_surface, settings.COLORS['PRIMARY'], send_btn)
            send_text = self.font_small.render("Type Message", True, settings.COLORS['WHITE'])
            send_text_rect = send_text.get_rect(center=send_btn.center)
            bottom_surface.blit(send_text, send_text_rect)
