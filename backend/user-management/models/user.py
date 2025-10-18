from dataclasses import dataclass
from typing import Optional
from datetime import datetime, UTC

@dataclass
class User:
    id: Optional[int] = None
    employee_id: str = ""
    email: str = ""
    password_hash: Optional[str] = None
    first_name: str = ""
    last_name: str = ""
    job_title: Optional[str] = None
    department: Optional[str] = None
    is_active: bool = True
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'job_title': self.job_title,
            'department': self.department,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }