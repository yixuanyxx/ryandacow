from dataclasses import dataclass
from typing import Optional
from datetime import datetime, UTC

@dataclass
class MentorshipRequest:
    id: Optional[int] = None
    mentee_id: Optional[int] = None
    mentor_id: Optional[int] = None
    status: str = "pending"
    message: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'mentee_id': self.mentee_id,
            'mentor_id': self.mentor_id,
            'status': self.status,
            'message': self.message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
