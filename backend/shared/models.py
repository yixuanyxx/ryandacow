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
class Skill:
    id: Optional[int] = None
    specialization_id: Optional[int] = None
    name: str = ""
    description: Optional[str] = None
    is_active: bool = True
    created_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'specialization_id': self.specialization_id,
            'name': self.name,
            'description': self.description,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

@dataclass
class UserSkill:
    id: Optional[int] = None
    user_id: Optional[int] = None
    skill_id: Optional[int] = None
    proficiency_level: int = 1
    years_experience: Optional[float] = None
    last_used: Optional[datetime] = None
    is_certified: bool = False
    certification_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'skill_id': self.skill_id,
            'proficiency_level': self.proficiency_level,
            'years_experience': self.years_experience,
            'last_used': self.last_used.isoformat() if self.last_used else None,
            'is_certified': self.is_certified,
            'certification_date': self.certification_date.isoformat() if self.certification_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

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
