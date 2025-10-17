import sys
sys.path.append('..')
from repo.career_repo import CareerRepo
from typing import Dict, Any, Optional

class CareerService:
    def __init__(self, career_repo: Optional[CareerRepo] = None):
        self.career_repo = career_repo or CareerRepo()
    
    def get_all_pathways(self) -> Dict[str, Any]:
        """Get all career pathways"""
        pathways = self.career_repo.get_all_pathways()
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": pathways
        }

    def get_pathway_recommendations(self, user_id: int) -> Dict[str, Any]:
        """Get career pathway recommendations based on user skills"""
        # Mock implementation - in real version would calculate based on user skills
        pathways = self.career_repo.get_all_pathways()
        
        recommendations = []
        for pathway in pathways[:3]:  # Top 3 for demo
            recommendations.append({
                'pathway': pathway,
                'match_score': 0.8,  # Mock score
                'requirements_met': [],
                'skill_gaps': []
            })
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": {
                "recommendations": recommendations,
                "user_skills_count": 0
            }
        }
