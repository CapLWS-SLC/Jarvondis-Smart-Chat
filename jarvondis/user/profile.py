# User profile and preference management with learning
import json
from datetime import datetime
from typing import Dict, List, Optional
import uuid

class UserProfile:
    """Manages user data, preferences, and learning history."""
    
    def __init__(self, user_id: str = None, email: str = None, name: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.email = email
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # Preference tracking
        self.preferences = {
            "language": "en",
            "tone": "neutral",  # neutral, formal, casual, friendly
            "response_length": "medium",  # short, medium, long
            "learning_mode": True,
            "accessibility": {
                "screen_reader_compatible": True,
                "high_contrast": False,
                "larger_text": False
            }
        }
        
        # Learning data - tracks what the AI learns about the user
        self.learning_data = {
            "interests": [],  # Topics of interest
            "skills": [],  # Skills the user wants to learn or already has
            "interaction_style": {},  # How user prefers to interact
            "expertise_level": {},  # Topics and expertise levels
            "communication_patterns": {}  # Learned communication preferences
        }
        
        # Unlocked skills
        self.unlocked_skills = ["search", "calculate", "summarize", "keywords"]
        self.skill_proficiency = {}  # Track proficiency in each skill
        
        # Interaction history for learning
        self.interaction_count = 0
        self.last_interaction = None
    
    def update_preference(self, key: str, value: any):
        """Update a user preference."""
        self.preferences[key] = value
        self.updated_at = datetime.utcnow()
    
    def add_interest(self, topic: str, confidence: float = 0.5):
        """Add or update user interest."""
        self.learning_data["interests"].append({
            "topic": topic,
            "confidence": confidence,
            "timestamp": datetime.utcnow().isoformat()
        })
        # Keep only top 50 interests
        if len(self.learning_data["interests"]) > 50:
            self.learning_data["interests"] = self.learning_data["interests"][-50:]
    
    def add_skill(self, skill_name: str, proficiency: float = 0.0):
        """Track a user skill with proficiency level (0-1)."""
        self.skill_proficiency[skill_name] = {
            "level": max(0, min(1, proficiency)),
            "last_updated": datetime.utcnow().isoformat(),
            "practice_count": self.skill_proficiency.get(skill_name, {}).get("practice_count", 0) + 1
        }
    
    def unlock_skill(self, skill_name: str):
        """Unlock a new skill for the user."""
        if skill_name not in self.unlocked_skills:
            self.unlocked_skills.append(skill_name)
            self.add_skill(skill_name, proficiency=0.1)
            return True
        return False
    
    def record_interaction(self, interaction_type: str, topic: str = None, success: bool = True):
        """Record an interaction for learning."""
        self.interaction_count += 1
        self.last_interaction = {
            "type": interaction_type,
            "topic": topic,
            "success": success,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def update_communication_pattern(self, pattern_type: str, value: any):
        """Learn about user's communication patterns."""
        self.learning_data["communication_patterns"][pattern_type] = {
            "value": value,
            "updated_at": datetime.utcnow().isoformat()
        }
    
    def to_dict(self) -> Dict:
        """Serialize user profile to dictionary."""
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "preferences": self.preferences,
            "learning_data": self.learning_data,
            "unlocked_skills": self.unlocked_skills,
            "skill_proficiency": self.skill_proficiency,
            "interaction_count": self.interaction_count,
            "last_interaction": self.last_interaction
        }
