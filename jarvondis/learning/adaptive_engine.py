# Enhanced learning engine that adapts to user behavior
import json
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict

class AdaptivelearningEngine:
    """AI learning engine that customizes to user needs like Microsoft Copilot."""
    
    def __init__(self):
        self.user_profiles = {}  # user_id -> profile
        self.interaction_history = defaultdict(list)
        self.topic_clusters = {}  # group similar topics
        self.skill_recommendations = {}  # user_id -> recommended skills
    
    def analyze_user_behavior(self, user_id: str, profile: 'UserProfile') -> Dict:
        """Analyze user behavior to personalize AI responses."""
        interactions = self.interaction_history.get(user_id, [])
        
        analysis = {
            "total_interactions": len(interactions),
            "primary_topics": self._extract_primary_topics(interactions),
            "skill_progression": self._analyze_skill_progression(profile),
            "learning_pace": self._calculate_learning_pace(interactions),
            "engagement_level": self._calculate_engagement(interactions),
            "recommended_skills": self._recommend_skills(profile, interactions)
        }
        
        return analysis
    
    def _extract_primary_topics(self, interactions: List[Dict]) -> List[str]:
        """Extract user's main areas of interest."""
        topics = defaultdict(int)
        for interaction in interactions[-50:]:  # Last 50 interactions
            if "topic" in interaction:
                topics[interaction["topic"]] += 1
        
        # Return top 5 topics
        return sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]
    
    def _analyze_skill_progression(self, profile: 'UserProfile') -> Dict:
        """Analyze how user's skills are progressing."""
        progression = {}
        for skill, proficiency_data in profile.skill_proficiency.items():
            progression[skill] = {
                "level": proficiency_data["level"],
                "practice_count": proficiency_data["practice_count"],
                "last_updated": proficiency_data["last_updated"]
            }
        return progression
    
    def _calculate_learning_pace(self, interactions: List[Dict]) -> str:
        """Determine user's learning pace (slow, medium, fast)."""
        if len(interactions) < 10:
            return "unknown"
        
        # Count interactions in last 7 days
        recent_count = sum(1 for i in interactions[-7:])
        
        if recent_count > 20:
            return "fast"
        elif recent_count > 10:
            return "medium"
        else:
            return "slow"
    
    def _calculate_engagement(self, interactions: List[Dict]) -> float:
        """Calculate engagement level 0-1."""
        if not interactions:
            return 0.0
        
        recent_interactions = interactions[-30:]
        success_count = sum(1 for i in recent_interactions if i.get("success", False))
        
        return min(1.0, success_count / len(recent_interactions)) if recent_interactions else 0.0
    
    def _recommend_skills(self, profile: 'UserProfile', interactions: List[Dict]) -> List[Dict]:
        """Recommend skills based on user behavior and interests."""
        recommendations = []
        
        # Skill recommendation logic
        unlocked_count = len(profile.unlocked_skills)
        interaction_count = profile.interaction_count
        
        # If user has high engagement, recommend advanced skills
        engagement = self._calculate_engagement(interactions)
        if engagement > 0.7 and unlocked_count >= 3:
            recommendations.append({
                "skill": "code_explain",
                "reason": "You're progressing well! Try explaining code.",
                "confidence": 0.8
            })
        
        if engagement > 0.8 and "summarize" in profile.unlocked_skills:
            recommendations.append({
                "skill": "brainstorm",
                "reason": "You're ready for creative thinking tools.",
                "confidence": 0.75
            })
        
        return recommendations
    
    def personalize_response(self, user_id: str, profile: 'UserProfile', 
                            base_response: str) -> str:
        """Personalize AI response based on user profile."""
        # Apply user's tone preference
        if profile.preferences.get("tone") == "formal":
            base_response = self._formalize_response(base_response)
        elif profile.preferences.get("tone") == "casual":
            base_response = self._casualize_response(base_response)
        
        # Adjust response length
        response_length = profile.preferences.get("response_length", "medium")
        if response_length == "short":
            base_response = base_response[:200] + "..."
        elif response_length == "long" and len(base_response) < 500:
            base_response += "\n\n[More details available upon request]"
        
        return base_response
    
    def _formalize_response(self, response: str) -> str:
        """Make response more formal."""
        # Simple formalization (can be enhanced with NLP)
        response = response.replace("hi", "Hello")
        response = response.replace("hey", "Greetings")
        return response
    
    def _casualize_response(self, response: str) -> str:
        """Make response more casual."""
        response = response.replace("Hello", "Hey")
        response = response.replace("Therefore", "So")
        return response
    
    def track_interaction(self, user_id: str, interaction_data: Dict):
        """Track user interaction for learning."""
        interaction_data["timestamp"] = datetime.utcnow().isoformat()
        self.interaction_history[user_id].append(interaction_data)
    
    def get_personalized_recommendations(self, user_id: str, profile: 'UserProfile') -> List[Dict]:
        """Get personalized skill and content recommendations."""
        analysis = self.analyze_user_behavior(user_id, profile)
        return analysis.get("recommended_skills", [])
