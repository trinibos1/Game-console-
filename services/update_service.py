"""
Auto-Update Service for Gaming System
"""

import os
import time
import subprocess
from config import settings

class UpdateService:
    def __init__(self):
        self.last_check = 0
        self.update_available = False
        self.current_version = "1.0.0"
        self.latest_version = "1.0.0"
    
    def check_for_updates(self):
        if not settings.SYSTEM['AUTO_UPDATE']:
            return False
        
        current_time = time.time()
        if current_time - self.last_check < settings.SYSTEM['UPDATE_CHECK_INTERVAL']:
            return self.update_available
        
        self.last_check = current_time
        
        try:
            result = subprocess.run(
                ['git', 'fetch', 'origin'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            result = subprocess.run(
                ['git', 'rev-list', 'HEAD...origin/main', '--count'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            commits_behind = int(result.stdout.strip())
            self.update_available = commits_behind > 0
            
            return self.update_available
        except Exception as e:
            print(f"Update check failed: {e}")
            return False
    
    def apply_update(self):
        if not self.update_available:
            return False
        
        try:
            subprocess.run(['git', 'pull', 'origin', 'main'], check=True)
            print("✅ Update applied successfully! Please restart the system.")
            return True
        except Exception as e:
            print(f"❌ Update failed: {e}")
            return False
    
    def get_update_status(self):
        return {
            'available': self.update_available,
            'current_version': self.current_version,
            'latest_version': self.latest_version
        }
