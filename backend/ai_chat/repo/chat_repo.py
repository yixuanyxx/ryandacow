import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from shared.database import get_db_connection
from datetime import datetime, UTC

class ChatRepo:
    def __init__(self):
        self.db = get_db_connection()
        self.demo_store = {"sessions": {}, "messages": []}

    def get_user_session(self, user_id: int):
        if not self.db.ready():
            return self.demo_store["sessions"].get(user_id)
        # 🔵 Real DB version
        res = self.db.client.table("ai_chat_sessions").select("*").eq("user_id", user_id).execute()
        return res.data[0] if res.data else None

    def create_session(self, payload: dict):
        if not self.db.ready():
            sid = payload["user_id"]
            self.demo_store["sessions"][sid] = {"id": sid, **payload}
            return self.demo_store["sessions"][sid]
        res = self.db.client.table("ai_chat_sessions").insert(payload).execute()
        return res.data[0]

    def create_message(self, payload: dict):
        if not self.db.ready():
            self.demo_store["messages"].append(payload)
            return payload
        self.db.client.table("ai_chat_messages").insert(payload).execute()
        return payload

    def get_session_messages_for_context(self, user_id, limit=6):
        session = self.get_user_session(user_id)
        if not session:
            return []
        msgs = self.db.table("ai_chat_messages") \
            .select("role,content") \
            .eq("session_id", session["id"]) \
            .order("created_at.desc") \
            .limit(limit) \
            .execute()
        return list(reversed(msgs.data or []))

    def get_user_profile(self, user_id: int):
        if not self.db.ready():
            return {
                "id": user_id,
                "first_name": "Demo",
                "job_title": "Engineer",
                "department": "IT",
            }
        res = self.db.client.table("users").select("*").eq("id", user_id).execute()
        return res.data[0] if res.data else None

    def get_user_skills(self, user_id: int):
        if not self.db.ready():
            return [{"skills": {"name": "Python"}}, {"skills": {"name": "System Design"}}]
        res = self.db.client.table("user_skills").select("*").eq("user_id", user_id).execute()
        return res.data or []