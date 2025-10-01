"""
App Registry for managing installed applications
"""

class AppRegistry:
    def __init__(self):
        self.apps = {}
        self.running_apps = {}
    
    def register(self, app_id, app_class):
        self.apps[app_id] = app_class
    
    def get_app(self, app_id):
        return self.apps.get(app_id)
    
    def launch_app(self, app_id):
        if app_id in self.apps:
            app_instance = self.apps[app_id]()
            self.running_apps[app_id] = app_instance
            return app_instance
        return None
    
    def get_all_apps(self):
        return [
            {'id': 'settings', 'name': 'Settings', 'icon': '⚙️'},
            {'id': 'music', 'name': 'Music', 'icon': '🎵'},
            {'id': 'friends', 'name': 'Friends', 'icon': '👥'},
            {'id': 'chat', 'name': 'Chat', 'icon': '💬'},
            {'id': 'browser', 'name': 'Browser', 'icon': '🌐'},
        ]
