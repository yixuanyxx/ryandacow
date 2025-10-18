import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any
import bcrypt

class AuthRepo:
    def __init__(self):
        self.db = get_db_connection()

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        res = self.db.table("users").select("*").eq("email", email).single().execute()
        return res.data

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        res = self.db.table("users").select("*").eq("id", user_id).single().execute()
        return res.data

    def update_last_login(self, user_id: int) -> bool:
        """Update last login timestamp"""
        res = self.db.table("users").update({
            "last_login": "now()"
        }).eq("id", user_id).execute()
        return len(res.data) > 0
