# User authentication and security
import hashlib
import secrets
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict
import re

class SecurityManager:
    """Handles user authentication, JWT tokens, and security validations."""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.algorithm = "HS256"
        self.token_expiry_hours = 24
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using SHA-256 with salt."""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${hash_obj.hex()}"
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash."""
        try:
            salt, hash_hex = hashed.split('$')
            hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return hash_obj.hex() == hash_hex
        except:
            return False
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Validate password strength."""
        if len(password) < 8:
            return False, "Password must be at least 8 characters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letter"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letter"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain number"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain special character"
        return True, "Password is strong"
    
    def create_token(self, user_id: str, email: str) -> str:
        """Create JWT token for authenticated user."""
        payload = {
            "user_id": user_id,
            "email": email,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict]:
        """Verify JWT token and return payload."""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def generate_verification_token(self, email: str) -> str:
        """Generate a token for email verification."""
        payload = {
            "email": email,
            "type": "email_verification",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def generate_reset_token(self, email: str) -> str:
        """Generate a token for password reset."""
        payload = {
            "email": email,
            "type": "password_reset",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
