from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, UTC

@dataclass
class Recommendation:
    id: Optional[int] = None
    user_id: Optional[int] = None
    type: str = ""  # 'course', 'mentor', 'career'
    title: str = ""
    description: str = ""
    match_score: Optional[float] = None
    metadata: Optional[dict] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'match_score': self.match_score,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
