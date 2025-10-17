import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class MentorshipRepo:
    def __init__(self):
        self.db = get_db_connection()

    def create_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create mentorship request"""
        res = self.db.table("mentorship_requests").insert(data).execute()
        if not res.data:
            raise RuntimeError("Mentorship request creation failed")
        return res.data[0]

    def get_user_requests(self, user_id: int) -> List[Dict[str, Any]]:
        """Get mentorship requests for user"""
        res = self.db.table("mentorship_requests").select("*").eq("mentee_id", user_id).execute()
        return res.data or []
