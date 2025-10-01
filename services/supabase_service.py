"""
Supabase Service for Database Operations
"""

import os
from supabase import create_client, Client
from config import settings

class SupabaseService:
    def __init__(self):
        self.client = None
        self.connected = False
        self.current_user = None
        
        try:
            supabase_url = os.getenv('SUPABASE_URL', '')
            supabase_key = os.getenv('SUPABASE_KEY', '')
            
            if supabase_url and supabase_key:
                self.client = create_client(supabase_url, supabase_key)
                self.connected = True
                print("✅ Connected to Supabase")
            else:
                print("⚠️  Supabase credentials not configured")
        except Exception as e:
            print(f"❌ Supabase connection failed: {e}")
    
    def is_connected(self):
        return self.connected
    
    def create_tables(self):
        if not self.client:
            return False
        
        try:
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            return False
    
    def get_friends(self, user_id):
        if not self.client:
            return []
        
        try:
            response = self.client.table('friends').select('*').eq('user_id', user_id).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching friends: {e}")
            return []
    
    def add_friend(self, user_id, friend_id):
        if not self.client:
            return False
        
        try:
            self.client.table('friends').insert({
                'user_id': user_id,
                'friend_id': friend_id,
                'status': 'pending'
            }).execute()
            return True
        except Exception as e:
            print(f"Error adding friend: {e}")
            return False
    
    def get_messages(self, user_id, friend_id):
        if not self.client:
            return []
        
        try:
            response = self.client.table('messages').select('*').or_(
                f'sender_id.eq.{user_id},receiver_id.eq.{user_id}'
            ).order('created_at').execute()
            return response.data
        except Exception as e:
            print(f"Error fetching messages: {e}")
            return []
    
    def send_message(self, sender_id, receiver_id, message):
        if not self.client:
            return False
        
        try:
            self.client.table('messages').insert({
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message': message
            }).execute()
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def update_user_status(self, user_id, status):
        if not self.client:
            return False
        
        try:
            self.client.table('users').update({
                'online_status': status
            }).eq('id', user_id).execute()
            return True
        except Exception as e:
            print(f"Error updating status: {e}")
            return False
