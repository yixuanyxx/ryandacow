import sys
sys.path.append('..')
from shared.auth import generate_token
from repo.user_repo import UserRepo, UserPersonalInfoRepo, EmploymentInfoRepo
from models.user import User
from typing import Dict, Any, Optional
from datetime import datetime, UTC
import hashlib
import secrets

class UserService:
    def __init__(self, user_repo: Optional[UserRepo] = None, 
                 personal_info_repo: Optional[UserPersonalInfoRepo] = None,
                 employment_repo: Optional[EmploymentInfoRepo] = None):
        self.user_repo = user_repo or UserRepo()
        self.personal_info_repo = personal_info_repo or UserPersonalInfoRepo()
        self.employment_repo = employment_repo or EmploymentInfoRepo()
    
    def register_user(self, payload: dict) -> dict:
        """Register a new user"""
        required_fields = ['employee_id', 'email', 'password', 'first_name', 'last_name']
        missing_fields = [field for field in required_fields if not payload.get(field)]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        # Check if user already exists
        existing_user = self.user_repo.get_user_by_email(payload['email'])
        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash password
        password_hash = self._hash_password(payload['password'])

        # Create user
        user_data = {
            'employee_id': payload['employee_id'],
            'email': payload['email'],
            'password_hash': password_hash,
            'first_name': payload['first_name'],
            'last_name': payload['last_name'],
            'is_active': True,
            'created_at': datetime.now(UTC).isoformat(),
            'updated_at': datetime.now(UTC).isoformat()
        }

        created_user = self.user_repo.create_user(user_data)
        
        return {
            "Code": 201,
            "Message": "User registered successfully",
            "data": {
                "user": created_user,
                "token": generate_token(created_user['id'])
            }
        }

    def login_user(self, email: str, password: str) -> dict:
        """Authenticate user login"""
        user_data = self.user_repo.get_user_by_email(email)
        
        if not user_data:
            return {"Code": 401, "Message": "Invalid email or password"}

        if not self._verify_password(password, user_data['password_hash']):
            return {"Code": 401, "Message": "Invalid email or password"}

        if not user_data['is_active']:
            return {"Code": 403, "Message": "Account is deactivated"}

        # Update last login
        self.user_repo.update_last_login(user_data['id'])

        return {
            "Code": 200,
            "Message": "Login successful",
            "data": {
                "user": user_data,
                "token": generate_token(user_data['id'])
            }
        }

    def get_user_profile(self, user_id: int) -> dict:
        """Get complete user profile"""
        user_data = self.user_repo.get_user_by_id(user_id)
        if not user_data:
            return {"Code": 404, "Message": "User not found"}

        # Get additional profile data
        personal_info = self.personal_info_repo.get_profile_by_user_id(user_id)
        employment = self.employment_repo.get_employment_by_user_id(user_id)

        return {
            "Code": 200,
            "Message": "Success",
            "data": {
                "user": user_data,
                "personal_info": personal_info,
                "employment": employment
            }
        }

    def update_profile(self, user_id: int, payload: dict) -> dict:
        """Update user profile"""
        user_data = self.user_repo.get_user_by_id(user_id)
        if not user_data:
            return {"Code": 404, "Message": "User not found"}

        # Update user basic info
        user_updates = {}
        if 'first_name' in payload:
            user_updates['first_name'] = payload['first_name']
        if 'last_name' in payload:
            user_updates['last_name'] = payload['last_name']

        if user_updates:
            user_updates['updated_at'] = datetime.now(UTC).isoformat()
            self.user_repo.update_user(user_id, user_updates)

        # Update personal info
        if any(key in payload for key in ['office_location', 'bio', 'profile_photo_url', 'phone']):
            personal_updates = {}
            personal_fields = ['office_location', 'bio', 'profile_photo_url', 'phone']
            
            for field in personal_fields:
                if field in payload:
                    personal_updates[field] = payload[field]

            if personal_updates:
                personal_updates['updated_at'] = datetime.now(UTC).isoformat()
                self.personal_info_repo.update_profile(user_id, personal_updates)

        return {"Code": 200, "Message": "Profile updated successfully"}

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"

    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_part = password_hash.split(':')
            return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
        except:
            return False
