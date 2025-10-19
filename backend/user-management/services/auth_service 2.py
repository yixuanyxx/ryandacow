import sys
sys.path.append('..')
from shared.auth import generate_token
from repo.auth_repo import AuthRepo
from typing import Dict, Any, Optional
import bcrypt

class AuthService:
    def __init__(self, auth_repo: Optional[AuthRepo] = None):
        self.auth_repo = auth_repo or AuthRepo()
    
    def login_user(self, email: str, password: str) -> dict:
        """Authenticate user login - MVP version with demo accounts"""
        try:
            user_data = self.auth_repo.get_user_by_email(email)
            
            if not user_data:
                return {"Code": 401, "Message": "Invalid email or password"}

            # For MVP, check if password matches demo password
            if password != 'demo123':
                return {"Code": 401, "Message": "Invalid email or password"}

            # Generate token using user ID (which is the employee ID in your case)
            token = generate_token(user_data['id'])

            return {
                "Code": 200,
                "Message": "Login successful",
                "data": {
                    "user": {
                        "id": user_data['id'],
                        "email": user_data['email'],
                        "name": user_data['name'],
                        "job_title": user_data['job_title'],
                        "department": user_data['department'],
                        "unit": user_data['unit'],
                        "line_manager": user_data['line_manager']
                    },
                    "token": token
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Internal server error: {str(e)}"}

    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile for dashboard - MVP version"""
        try:
            user_data = self.auth_repo.get_user_by_id(user_id)
            if not user_data:
                return {"Code": 404, "Message": "User not found"}

            # Get user skills
            user_skills = self.auth_repo.get_user_skills(user_id)

            return {
                "Code": 200,
                "Message": "Success",
                "data": {
                    "user": {
                        "id": user_data['id'],
                        "email": user_data['email'],
                        "name": user_data['name'],
                        "job_title": user_data['job_title'],
                        "department": user_data['department'],
                        "unit": user_data['unit'],
                        "line_manager": user_data['line_manager'],
                        "in_role_since": user_data['in_role_since'],
                        "hire_date": user_data['hire_date'],
                        "last_updated": user_data['last_updated']
                    },
                    "skills": user_skills
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Internal server error: {str(e)}"}