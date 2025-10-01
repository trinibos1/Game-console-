#!/usr/bin/env python3
"""
Nintendo 3DS-Inspired Gaming System for Raspberry Pi
Main application entry point
"""

import os
import sys
import pygame
from dotenv import load_dotenv

load_dotenv()

from config import settings
from ui.screen_manager import ScreenManager
from ui.input_handler import InputHandler
from services.notification_service import NotificationService
from services.app_registry import AppRegistry
from services.update_service import UpdateService

class GamingSystem:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        
        try:
            pygame.mixer.init()
        except pygame.error:
            print("⚠️  Audio device not available, running without sound")
        
        self.running = True
        self.clock = pygame.time.Clock()
        
        self.screen_manager = ScreenManager()
        self.input_handler = InputHandler()
        self.notification_service = NotificationService()
        self.app_registry = AppRegistry()
        self.update_service = UpdateService()
        
        self.register_apps()
        self.check_updates()
    
    def register_apps(self):
        from apps.settings.settings_app import SettingsApp
        from apps.music.music_app import MusicApp
        from apps.friends.friends_app import FriendsApp
        from apps.chat.chat_app import ChatApp
        from apps.browser.browser_app import BrowserApp
        
        self.app_registry.register('settings', SettingsApp)
        self.app_registry.register('music', MusicApp)
        self.app_registry.register('friends', FriendsApp)
        self.app_registry.register('chat', ChatApp)
        self.app_registry.register('browser', BrowserApp)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            self.input_handler.handle_event(event)
            self.screen_manager.handle_event(event)
        
        buttons = self.input_handler.get_button_states()
        if buttons.get('HOME'):
            self.screen_manager.go_home()
        if buttons.get('POWER'):
            self.running = False
    
    def check_updates(self):
        if settings.SYSTEM['AUTO_UPDATE']:
            if self.update_service.check_for_updates():
                print("🔄 Update available! Check Settings > System to update.")
    
    def update(self, dt):
        self.screen_manager.update(dt)
        self.notification_service.update(dt)
    
    def render(self):
        self.screen_manager.render()
        pygame.display.flip()
    
    def run(self):
        print("🎮 Gaming System Starting...")
        print(f"   Top Screen: {settings.DISPLAY['TOP_WIDTH']}x{settings.DISPLAY['TOP_HEIGHT']}")
        print(f"   Bottom Screen: {settings.DISPLAY['BOTTOM_WIDTH']}x{settings.DISPLAY['BOTTOM_HEIGHT']}")
        
        while self.running:
            dt = self.clock.tick(settings.DISPLAY['FPS']) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        print("🛑 Gaming System Shutting Down...")
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    app = GamingSystem()
    app.run()
