import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class RecommendationsRepo:
    def __init__(self):
        self.db = get_db_connection()

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile"""
        res = self.db.table("users").select("*").eq("id", user_id).single().execute()
        return res.data

    def get_user_skills(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's skills"""
        res = self.db.table("user_skills").select("""
            *,
            skills(*)
        """).eq("user_id", user_id).execute()
        return res.data or []

    def get_courses(self) -> List[Dict[str, Any]]:
        """Get all courses"""
        res = self.db.table("courses").select("*").execute()
        return res.data or []

    def get_career_pathways(self) -> List[Dict[str, Any]]:
        """Get all career pathways"""
        res = self.db.table("career_pathways").select("*").execute()
        return res.data or []

    def get_potential_mentors(self, user_id: str) -> List[Dict[str, Any]]:
        """Get potential mentors (other users with higher skills)"""
        res = self.db.table("users").select("""
            *,
            user_skills(
                *,
                skills(*)
            )
        """).neq("id", user_id).execute()
        return res.data or []
