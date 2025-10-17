import sys
sys.path.append('..')
from repo.skills_repo import SkillsRepo
from typing import Dict, Any, Optional
from datetime import datetime, UTC

class SkillsService:
    def __init__(self, skills_repo: Optional[SkillsRepo] = None):
        self.skills_repo = skills_repo or SkillsRepo()
    
    def get_all_skills(self) -> Dict[str, Any]:
        """Get all skills with their specializations and function areas"""
        skills = self.skills_repo.get_all_skills()
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": skills
        }

    def get_user_skills(self, user_id: int) -> Dict[str, Any]:
        """Get user's skills with proficiency levels"""
        user_skills = self.skills_repo.get_user_skills(user_id)
        
        # Group skills by function area
        skills_by_category = {}
        for skill_data in user_skills:
            skill_info = skill_data.get('skills', {})
            specialization = skill_info.get('specializations', {})
            function_area = specialization.get('function_areas', {})
            category = function_area.get('name', 'Other')
            
            if category not in skills_by_category:
                skills_by_category[category] = []
            
            skills_by_category[category].append({
                'id': skill_data['id'],
                'skill_id': skill_data['skill_id'],
                'skill_name': skill_info.get('name', ''),
                'proficiency_level': skill_data['proficiency_level'],
                'years_experience': skill_data.get('years_experience', 0),
                'is_certified': skill_data.get('is_certified', False),
                'specialization': specialization.get('name', ''),
                'function_area': category
            })

        return {
            "Code": 200,
            "Message": "Success",
            "data": {
                "skills_by_category": skills_by_category,
                "total_skills": len(user_skills)
            }
        }

    def add_user_skill(self, user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Add skill to user's profile"""
        required_fields = ['skill_id', 'proficiency_level']
        missing_fields = [field for field in required_fields if not payload.get(field)]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        skill_data = {
            'user_id': user_id,
            'skill_id': payload['skill_id'],
            'proficiency_level': payload['proficiency_level'],
            'years_experience': payload.get('years_experience'),
            'is_certified': payload.get('is_certified', False),
            'created_at': datetime.now(UTC).isoformat(),
            'updated_at': datetime.now(UTC).isoformat()
        }

        created_skill = self.skills_repo.add_user_skill(skill_data)
        
        return {
            "Code": 201,
            "Message": "Skill added successfully",
            "data": created_skill
        }
