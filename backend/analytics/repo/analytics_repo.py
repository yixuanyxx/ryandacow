import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class AnalyticsRepo:
    def __init__(self):
        self.db = get_db_connection()

    def get_user_analytics(self, user_id: int) -> List[Dict[str, Any]]:
        """Get analytics data for user"""
        res = self.db.table("user_analytics").select("*").eq("user_id", user_id).order("recorded_at", desc=True).execute()
        return res.data or []

    def record_analytics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Record analytics data"""
        res = self.db.table("user_analytics").insert(data).execute()
        if not res.data:
            raise RuntimeError("Analytics recording failed")
        return res.data[0]
