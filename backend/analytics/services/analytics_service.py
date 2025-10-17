import sys
sys.path.append('..')
from repo.analytics_repo import AnalyticsRepo
from typing import Dict, Any, Optional
from datetime import datetime, UTC

class AnalyticsService:
    def __init__(self, analytics_repo: Optional[AnalyticsRepo] = None):
        self.analytics_repo = analytics_repo or AnalyticsRepo()
    
    def get_dashboard_data(self, user_id: int) -> Dict[str, Any]:
        """Get dashboard analytics data"""
        # Mock dashboard data
        dashboard_data = {
            "skills_progress": {
                "total_skills": 15,
                "completed_skills": 8,
                "in_progress_skills": 4,
                "not_started_skills": 3
            },
            "learning_velocity": {
                "courses_completed": 3,
                "hours_learned": 24,
                "current_streak": 7
            },
            "career_metrics": {
                "goals_set": 2,
                "goals_completed": 1,
                "mentorship_requests": 1,
                "leadership_score": 75
            }
        }
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": dashboard_data
        }

    def get_user_metrics(self, user_id: int) -> Dict[str, Any]:
        """Get detailed user metrics"""
        analytics_data = self.analytics_repo.get_user_analytics(user_id)
        
        # Mock metrics
        metrics = {
            "engagement_score": 85,
            "learning_velocity": 2.3,
            "skill_growth_rate": 15,
            "career_progression": 60,
            "mentorship_activity": 3,
            "training_completion_rate": 0.8
        }
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": {
                "metrics": metrics,
                "analytics_history": analytics_data
            }
        }
