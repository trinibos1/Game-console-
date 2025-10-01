"""
Game Scanner for Auto-Detecting Games from Folders
"""

import os
import json
from pathlib import Path
from config import settings

class GameScanner:
    def __init__(self):
        self.games_path = settings.PATHS['GAMES']
        self.games = []
        self.scan_games()
    
    def scan_games(self):
        self.games = []
        
        if not self.games_path.exists():
            self.games_path.mkdir(parents=True, exist_ok=True)
            return
        
        for item in self.games_path.iterdir():
            if item.is_dir():
                game_info = self.load_game_info(item)
                if game_info:
                    self.games.append(game_info)
            elif item.suffix in ['.sh', '.py', '.bin']:
                game_info = {
                    'id': item.stem,
                    'name': item.stem.replace('_', ' ').title(),
                    'path': str(item),
                    'executable': str(item),
                    'icon': '🎮',
                    'description': 'Game',
                }
                self.games.append(game_info)
        
        self.games.sort(key=lambda x: x['name'])
    
    def load_game_info(self, game_dir):
        info_file = game_dir / 'game.json'
        
        if info_file.exists():
            try:
                with open(info_file, 'r') as f:
                    info = json.load(f)
                    info['path'] = str(game_dir)
                    return info
            except Exception as e:
                print(f"Error loading game info: {e}")
        
        executable = None
        for ext in ['.sh', '.py', '.bin', 'start.sh', 'run.sh']:
            potential_exe = game_dir / ext
            if potential_exe.exists():
                executable = str(potential_exe)
                break
        
        if executable:
            return {
                'id': game_dir.name,
                'name': game_dir.name.replace('_', ' ').title(),
                'path': str(game_dir),
                'executable': executable,
                'icon': '🎮',
                'description': f'Game in {game_dir.name}',
            }
        
        return None
    
    def get_games(self):
        return self.games
    
    def launch_game(self, game_id):
        game = next((g for g in self.games if g['id'] == game_id), None)
        if game and 'executable' in game:
            try:
                import subprocess
                subprocess.Popen([game['executable']], cwd=game['path'])
                return True
            except Exception as e:
                print(f"Error launching game: {e}")
        return False
