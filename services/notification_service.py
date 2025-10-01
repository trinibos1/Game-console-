"""
Notification Service for system-wide notifications
"""

class NotificationService:
    def __init__(self):
        self.notifications = []
        self.badges = {}
    
    def add_notification(self, title, message, icon=None):
        notification = {
            'title': title,
            'message': message,
            'icon': icon,
            'timestamp': 0
        }
        self.notifications.append(notification)
    
    def set_badge(self, app_name, count):
        self.badges[app_name] = count
    
    def get_badge(self, app_name):
        return self.badges.get(app_name, 0)
    
    def update(self, dt):
        pass
