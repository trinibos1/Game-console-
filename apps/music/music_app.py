"""
Music Player Application with Playlist Management
"""

import pygame
from pathlib import Path
from config import settings

class MusicApp:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager
        self.name = "Music"
        self.icon = "🎵"
        
        self.font_small = pygame.font.Font(None, settings.FONTS['SMALL'])
        self.font_medium = pygame.font.Font(None, settings.FONTS['MEDIUM'])
        self.font_large = pygame.font.Font(None, settings.FONTS['LARGE'])
        
        self.playlist = []
        self.current_track = 0
        self.playing = False
        self.volume = settings.AUDIO['DEFAULT_VOLUME']
        
        self.scan_music()
    
    def scan_music(self):
        music_path = settings.PATHS['DATA'] / 'music'
        if not music_path.exists():
            music_path.mkdir(parents=True, exist_ok=True)
            return
        
        for ext in settings.AUDIO['MUSIC_FORMATS']:
            self.playlist.extend([str(f) for f in music_path.glob(f'*{ext}')])
        
        self.playlist.sort()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.toggle_play()
            elif event.key == pygame.K_RIGHT:
                self.next_track()
            elif event.key == pygame.K_LEFT:
                self.previous_track()
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
        
        prev_btn = pygame.Rect(40, 180, 60, 40)
        play_btn = pygame.Rect(110, 180, 60, 40)
        next_btn = pygame.Rect(180, 180, 60, 40)
        
        if prev_btn.collidepoint(touch_x, touch_y):
            self.previous_track()
        elif play_btn.collidepoint(touch_x, touch_y):
            self.toggle_play()
        elif next_btn.collidepoint(touch_x, touch_y):
            self.next_track()
    
    def toggle_play(self):
        if not self.playlist:
            return
        
        self.playing = not self.playing
        
        try:
            if self.playing:
                if 0 <= self.current_track < len(self.playlist):
                    pygame.mixer.music.load(self.playlist[self.current_track])
                    pygame.mixer.music.play()
            else:
                pygame.mixer.music.pause()
        except Exception as e:
            print(f"Music playback error: {e}")
    
    def next_track(self):
        if not self.playlist:
            return
        self.current_track = (self.current_track + 1) % len(self.playlist)
        if self.playing:
            self.playing = False
            self.toggle_play()
    
    def previous_track(self):
        if not self.playlist:
            return
        self.current_track = (self.current_track - 1) % len(self.playlist)
        if self.playing:
            self.playing = False
            self.toggle_play()
    
    def update(self, dt):
        pass
    
    def render(self, top_surface, bottom_surface):
        top_surface.fill(settings.COLORS['DARK'])
        
        title = self.font_large.render("🎵 Music Player", True, settings.COLORS['WHITE'])
        top_surface.blit(title, (20, 20))
        
        if self.playlist:
            if 0 <= self.current_track < len(self.playlist):
                track_name = Path(self.playlist[self.current_track]).stem
                track_surf = self.font_medium.render(track_name, True, settings.COLORS['WHITE'])
                track_rect = track_surf.get_rect(center=(top_surface.get_width() // 2, 150))
                top_surface.blit(track_surf, track_rect)
            
            status = "▶️ Playing" if self.playing else "⏸️ Paused"
            status_surf = self.font_small.render(status, True, settings.COLORS['SUCCESS'] if self.playing else settings.COLORS['GRAY'])
            status_rect = status_surf.get_rect(center=(top_surface.get_width() // 2, 200))
            top_surface.blit(status_surf, status_rect)
        else:
            no_music = self.font_medium.render("No music files found", True, settings.COLORS['GRAY'])
            no_music_rect = no_music.get_rect(center=(top_surface.get_width() // 2, 150))
            top_surface.blit(no_music, no_music_rect)
        
        bottom_surface.fill(settings.COLORS['DARK'])
        
        if self.playlist:
            playlist_title = self.font_small.render("Playlist:", True, settings.COLORS['WHITE'])
            bottom_surface.blit(playlist_title, (10, 10))
            
            y = 35
            for i, track in enumerate(self.playlist[:5]):
                track_name = Path(track).stem[:25]
                color = settings.COLORS['PRIMARY'] if i == self.current_track else settings.COLORS['WHITE']
                track_surf = self.font_small.render(f"{i+1}. {track_name}", True, color)
                bottom_surface.blit(track_surf, (10, y))
                y += 20
        
        prev_btn = pygame.Rect(40, 180, 60, 40)
        play_btn = pygame.Rect(110, 180, 60, 40)
        next_btn = pygame.Rect(180, 180, 60, 40)
        
        pygame.draw.rect(bottom_surface, settings.COLORS['SECONDARY'], prev_btn)
        pygame.draw.rect(bottom_surface, settings.COLORS['PRIMARY'], play_btn)
        pygame.draw.rect(bottom_surface, settings.COLORS['SECONDARY'], next_btn)
        
        prev_text = self.font_medium.render("⏮️", True, settings.COLORS['WHITE'])
        play_text = self.font_medium.render("▶️" if not self.playing else "⏸️", True, settings.COLORS['WHITE'])
        next_text = self.font_medium.render("⏭️", True, settings.COLORS['WHITE'])
        
        bottom_surface.blit(prev_text, (prev_btn.centerx - 10, prev_btn.centery - 10))
        bottom_surface.blit(play_text, (play_btn.centerx - 10, play_btn.centery - 10))
        bottom_surface.blit(next_text, (next_btn.centerx - 10, next_btn.centery - 10))
