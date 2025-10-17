import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class AIRepo:
    def __init__(self):
        self.db = get_db_connection()

    def create_chat_session(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new AI chat session"""
        res = self.db.table("ai_chat_sessions").insert(data).execute()
        if not res.data:
            raise RuntimeError("Chat session creation failed")
        return res.data[0]

    def get_user_sessions(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's chat sessions"""
        res = self.db.table("ai_chat_sessions").select("*").eq("user_id", user_id).order("created_at", desc=True).execute()
        return res.data or []
