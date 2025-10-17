from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime, UTC

@dataclass
class User:
    id: Optional[int] = None
    employee_id: str = ""
    email: str = ""
    password_hash: Optional[str] = None
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

@dataclass
class UserPersonalInfo:
    id: Optional[int] = None
    user_id: Optional[int] = None
    office_location: Optional[str] = None
    bio: Optional[str] = None
    profile_photo_url: Optional[str] = None
    phone: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'office_location': self.office_location,
            'bio': self.bio,
            'profile_photo_url': self.profile_photo_url,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

@dataclass
class EmploymentInfo:
    id: Optional[int] = None
    user_id: Optional[int] = None
    job_title: str = ""
    department: str = ""
    unit: Optional[str] = None
    line_manager: Optional[str] = None
    in_role_since: Optional[datetime] = None
    hire_date: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'job_title': self.job_title,
            'department': self.department,
            'unit': self.unit,
            'line_manager': self.line_manager,
            'in_role_since': self.in_role_since.isoformat() if self.in_role_since else None,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
