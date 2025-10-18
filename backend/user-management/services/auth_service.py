import sys
sys.path.append('..')
from shared.auth import generate_token
from repo.auth_repo import AuthRepo
from typing import Dict, Any, Optional
from datetime import datetime, UTC
import bcrypt

class AuthService:
    def __init__(self, auth_repo: Optional[AuthRepo] = None):
        self.auth_repo = auth_repo or AuthRepo()
    
    def login_user(self, email: str, password: str) -> dict:
        """Authenticate user login - MVP with demo accounts"""
        user_data = self.auth_repo.get_user_by_email(email)
        
        if not user_data:
            return {"Code": 401, "Message": "Invalid email or password"}

        # For MVP, accept any password for demo accounts
        # In production, verify password hash
        if not self._verify_password(password, user_data.get('password_hash', '')):
            return {"Code": 401, "Message": "Invalid email or password"}

        if not user_data['is_active']:
            return {"Code": 403, "Message": "Account is deactivated"}

        # Update last login
        self.auth_repo.update_last_login(user_data['id'])

        return {
            "Code": 200,
            "Message": "Login successful",
            "data": {
                "user": {
                    "id": user_data['id'],
                    "email": user_data['email'],
                    "first_name": user_data['first_name'],
                    "last_name": user_data['last_name'],
                    "job_title": user_data['job_title'],
                    "department": user_data['department']
                },
                "token": generate_token(user_data['id'])
            }
        }

    def get_user_profile(self, user_id: int) -> dict:
        """Get user profile for dashboard"""
        user_data = self.auth_repo.get_user_by_id(user_id)
        if not user_data:
            return {"Code": 404, "Message": "User not found"}

        return {
            "Code": 200,
            "Message": "Success",
            "data": {
                "id": user_data['id'],
                "email": user_data['email'],
                "first_name": user_data['first_name'],
                "last_name": user_data['last_name'],
                "job_title": user_data['job_title'],
                "department": user_data['department'],
                "full_name": f"{user_data['first_name']} {user_data['last_name']}"
            }
        }

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password - MVP version accepts any password"""
        # For MVP demo, accept any password
        return True
        # In production, use:
        # return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
