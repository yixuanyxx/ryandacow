import sys
sys.path.append('..')
from shared.database import get_db_connection
from typing import Optional, Dict, Any, List

class ChatRepo:
    def __init__(self):
        self.db = get_db_connection()

    def create_session(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new chat session"""
        res = self.db.table("ai_chat_sessions").insert(data).execute()
        if not res.data:
            raise RuntimeError("Chat session creation failed")
        return res.data[0]

    def get_user_session(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's active chat session"""
        res = self.db.table("ai_chat_sessions").select("*").eq("user_id", user_id).order("created_at", desc=True).limit(1).execute()
        return res.data[0] if res.data else None

    def create_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a chat message"""
        res = self.db.table("ai_chat_messages").insert(data).execute()
        if not res.data:
            raise RuntimeError("Message creation failed")
        return res.data[0]

    def get_session_messages(self, session_id: int) -> List[Dict[str, Any]]:
        """Get all messages for a session"""
        res = self.db.table("ai_chat_messages").select("*").eq("session_id", session_id).order("created_at").execute()
        return res.data or []

    def get_user_skills(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's skills for AI context"""
        res = self.db.table("user_skills").select("""
            *,
            skills(*)
        """).eq("user_id", user_id).execute()
        return res.data or []

    def get_user_profile(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user profile for AI context"""
        res = self.db.table("users").select("*").eq("id", user_id).single().execute()
        return res.data
