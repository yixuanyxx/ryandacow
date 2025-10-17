from dataclasses import dataclass
from typing import Optional
from datetime import datetime, UTC

@dataclass
class Course:
    id: Optional[int] = None
    title: str = ""
    description: Optional[str] = None
    duration_hours: Optional[int] = None
    difficulty_level: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'duration_hours': self.duration_hours,
            'difficulty_level': self.difficulty_level,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
