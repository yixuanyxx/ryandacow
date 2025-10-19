import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class UserRepo:
    def __init__(self):
        self.db = get_db_connection()

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        res = self.db.table("users").select("*").eq("email", email).single().execute()
        return res.data

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID (using employee ID as string)"""
        res = self.db.table("users").select("*").eq("id", user_id).single().execute()
        return res.data

    def get_user_skills(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's skills with skill details"""
        res = self.db.table("user_skills").select("""
            *,
            skills(*)
        """).eq("user_id", user_id).execute()
        return res.data or []

    def get_users_by_department(self, department: str) -> List[Dict[str, Any]]:
        """Get all users in a department"""
        res = self.db.table("users").select("*").eq("department", department).execute()
        return res.data or []

    def update_last_login(self, user_id: str) -> bool:
        """Update last login timestamp"""
        res = self.db.table("users").update({
            "last_login": "now()"
        }).eq("id", user_id).execute()
        return len(res.data) > 0

class UserPersonalInfoRepo:
    def __init__(self):
        self.db = get_db_connection()

    def create_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create user profile"""
        res = self.db.table("user_personal_info").insert(data).execute()
        if not res.data:
            raise RuntimeError("Profile creation failed – no data returned")
        return res.data[0]

    def get_profile_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get profile by user ID"""
        res = self.db.table("user_personal_info").select("*").eq("user_id", user_id).single().execute()
        return res.data

    def update_profile(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        res = self.db.table("user_personal_info").upsert({
            'user_id': user_id,
            **data
        }).execute()
        if not res.data:
            raise RuntimeError("Profile update failed – no data returned")
        return res.data[0]

class EmploymentInfoRepo:
    def __init__(self):
        self.db = get_db_connection()

    def create_employment_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create employment info"""
        res = self.db.table("employment_info").insert(data).execute()
        if not res.data:
            raise RuntimeError("Employment info creation failed – no data returned")
        return res.data[0]

    def get_employment_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get employment info by user ID"""
        res = self.db.table("employment_info").select("*").eq("user_id", user_id).single().execute()
        return res.data

    def update_employment_info(self, user_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update employment info"""
        res = self.db.table("employment_info").upsert({
            'user_id': user_id,
            **data
        }).execute()
        if not res.data:
            raise RuntimeError("Employment info update failed – no data returned")
        return res.data[0]
