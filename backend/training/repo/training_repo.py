import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class TrainingRepo:
    def __init__(self):
        self.db = get_db_connection()

    def get_courses(self) -> List[Dict[str, Any]]:
        """Get all active courses"""
        res = self.db.table("courses").select("*").eq("is_active", True).order("title").execute()
        return res.data or []

    def enroll_user(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Enroll user in course"""
        res = self.db.table("user_training").insert(data).execute()
        if not res.data:
            raise RuntimeError("Course enrollment failed")
        return res.data[0]
