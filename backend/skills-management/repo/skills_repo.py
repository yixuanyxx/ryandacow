import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class SkillsRepo:
    def __init__(self):
        self.db = get_db_connection()

    def get_all_skills(self) -> List[Dict[str, Any]]:
        """Get all active skills"""
        res = self.db.table("skills").select(`
            *,
            specializations(
                *,
                function_areas(*)
            )
        `).eq("is_active", True).order("name").execute()
        return res.data or []

    def get_user_skills(self, user_id: int) -> List[Dict[str, Any]]:
        """Get all skills for a user with skill details"""
        res = self.db.table("user_skills").select(`
            *,
            skills(
                *,
                specializations(
                    *,
                    function_areas(*)
                )
            )
        `).eq("user_id", user_id).execute()
        return res.data or []

    def add_user_skill(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Add skill to user"""
        res = self.db.table("user_skills").insert(data).execute()
        if not res.data:
            raise RuntimeError("Failed to add user skill")
        return res.data[0]

    def update_user_skill(self, user_skill_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user skill"""
        res = self.db.table("user_skills").update(data).eq("id", user_skill_id).execute()
        if not res.data:
            raise RuntimeError("Failed to update user skill")
        return res.data[0]

    def remove_user_skill(self, user_skill_id: int) -> bool:
        """Remove skill from user"""
        res = self.db.table("user_skills").delete().eq("id", user_skill_id).execute()
        return len(res.data) > 0
