from dataclasses import dataclass
from typing import Optional
from datetime import datetime, UTC

@dataclass
class CareerPathway:
    id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    department: Optional[str] = None
    level: Optional[str] = None
    min_years_experience: Optional[int] = None
    max_years_experience: Optional[int] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'department': self.department,
            'level': self.level,
            'min_years_experience': self.min_years_experience,
            'max_years_experience': self.max_years_experience,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
