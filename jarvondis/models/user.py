# Models for database/persistence
from datetime import datetime
from typing import Optional, Dict, List
from enum import Enum

class UserVerificationStatus(Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    BLOCKED = "blocked"

class UserModel:
    """User data model for persistence."""
    
    def __init__(self, email: str, name: str, password_hash: str,
                 user_id: str = None):
        self.user_id = user_id or str(uuid.uuid4())
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.verification_status = UserVerificationStatus.UNVERIFIED.value
        self.email_verified = False
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.last_login = None
        self.profile_data = {}
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": self.name,
            "verification_status": self.verification_status,
            "email_verified": self.email_verified,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "profile_data": self.profile_data
        }

import uuid
