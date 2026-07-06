# Database service for user management
from typing import Optional, List, Dict
import json
import os
from datetime import datetime

class UserDatabase:
    """Simple in-memory database for users (can be replaced with real DB)."""
    
    def __init__(self, db_file: str = None):
        self.db_file = db_file or "users.json"
        self.users = {}
        self.profiles = {}
        self.load_from_file()
    
    def load_from_file(self):
        """Load users from JSON file if exists."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    data = json.load(f)
                    self.users = data.get("users", {})
                    self.profiles = data.get("profiles", {})
            except:
                pass
    
    def save_to_file(self):
        """Save users to JSON file."""
        try:
            with open(self.db_file, 'w') as f:
                json.dump({
                    "users": self.users,
                    "profiles": self.profiles
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving to file: {str(e)}")
    
    def create_user(self, user_id: str, email: str, name: str, 
                   password_hash: str) -> bool:
        """Create new user."""
        if email in self.users:
            return False
        
        self.users[email] = {
            "user_id": user_id,
            "name": name,
            "password_hash": password_hash,
            "email_verified": False,
            "created_at": datetime.utcnow().isoformat(),
            "last_login": None
        }
        
        self.save_to_file()
        return True
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email."""
        return self.users.get(email)
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID."""
        for user in self.users.values():
            if user.get("user_id") == user_id:
                return user
        return None
    
    def update_user(self, email: str, updates: Dict) -> bool:
        """Update user information."""
        if email not in self.users:
            return False
        
        self.users[email].update(updates)
        self.save_to_file()
        return True
    
    def verify_email(self, email: str) -> bool:
        """Mark email as verified."""
        return self.update_user(email, {"email_verified": True})
    
    def save_profile(self, user_id: str, profile_data: Dict) -> bool:
        """Save user profile."""
        self.profiles[user_id] = profile_data
        self.save_to_file()
        return True
    
    def get_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile."""
        return self.profiles.get(user_id)
