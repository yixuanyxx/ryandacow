from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, UTC

@dataclass
class ChatSession:
    id: Optional[int] = None
    user_id: Optional[int] = None
    session_name: Optional[str] = None
    context_data: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_name': self.session_name,
            'context_data': self.context_data,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

@dataclass
class ChatMessage:
    id: Optional[int] = None
    session_id: Optional[int] = None
    role: str = ""  # 'user' or 'assistant'
    content: str = ""
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'session_id': self.session_id,
            'role': self.role,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
