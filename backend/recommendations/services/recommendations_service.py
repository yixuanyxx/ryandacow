import sys
sys.path.append('..')
from typing import Dict, Any, Optional, List
from datetime import datetime, UTC

class RecommendationsService:
    def __init__(self, repo: Optional[None] = None):
        # For MVP, we don't use the database repo
        pass
    
    def get_user_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get all recommendations for user dashboard - MVP version with demo data"""
        try:
            # Demo user data
            demo_users = {
                "EMP-20001": {"name": "Samantha Lee", "job_title": "Cloud Solutions Architect", "department": "Information Technology"},
                "EMP-20002": {"name": "Aisyah Rahman", "job_title": "Cybersecurity Analyst", "department": "Information Technology"},
                "EMP-20003": {"name": "Rohan Mehta", "job_title": "Finance Manager (FP&A)", "department": "Finance"},
                "EMP-20004": {"name": "Grace Lee", "job_title": "Senior HR Business Partner", "department": "Human Resource"},
                "EMP-20005": {"name": "Felicia Goh", "job_title": "Treasury Analyst", "department": "Finance"}
            }
            
            user_profile = demo_users.get(user_id, {"name": "Demo User", "job_title": "Employee", "department": "General"})

            # Demo recommendations
            recommendations = [
                {
                    "type": "course",
                    "title": "Leadership Fundamentals",
                    "description": "Develop essential leadership skills for career advancement",
                    "match_score": 92,
                    "metadata": {
                        "duration_weeks": 24,
                        "required_skills": ["Communication", "Team Management"]
                    }
                },
                {
                    "type": "mentor",
                    "title": "Michael Chen",
                    "description": "Senior Tech Lead with extensive experience in cloud architecture",
                    "match_score": 88,
                    "metadata": {
                        "job_title": "Senior Tech Lead",
                        "department": "Information Technology",
                        "experience_years": 15
                    }
                },
                {
                    "type": "career",
                    "title": "Senior Software Engineer",
                    "description": "Next step: Senior Software Engineer - Lead technical projects and mentor junior developers",
                    "match_score": 85,
                    "metadata": {
                        "target_role": "Senior Software Engineer",
                        "required_skills": ["System Design", "Team Leadership", "Technical Mentoring"]
                    }
                }
            ]

            return {
                "Code": 200,
                "Message": "Success",
                "data": {
                    "recommendations": recommendations,
                    "user_name": user_profile['name'],
                    "job_title": user_profile['job_title'],
                    "department": user_profile['department']
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error generating recommendations: {str(e)}"}

    def get_course_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized course recommendations - MVP version with demo data"""
        try:
            # Demo course recommendations
            recommendations = [
                {
                    "id": 1,
                    "title": "Leadership Fundamentals",
                    "description": "Develop essential leadership skills for career advancement",
                    "duration_weeks": 24,
                    "match_score": 92,
                    "required_skills": ["Communication", "Team Management"]
                },
                {
                    "id": 2,
                    "title": "System Design Masterclass",
                    "description": "Learn to design scalable and robust systems",
                    "duration_weeks": 32,
                    "match_score": 88,
                    "required_skills": ["Architecture", "Scalability", "Performance"]
                },
                {
                    "id": 3,
                    "title": "Advanced Python for Leaders",
                    "description": "Master Python programming for senior technical roles",
                    "duration_weeks": 40,
                    "match_score": 85,
                    "required_skills": ["Python", "Advanced Programming", "Code Review"]
                }
            ]

            return {
                "Code": 200,
                "Message": "Success",
                "data": recommendations
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error getting course recommendations: {str(e)}"}

    def get_mentor_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get mentor recommendations - MVP version with demo data"""
        try:
            # Demo mentor recommendations
            recommendations = [
                {
                    "id": 1,
                    "name": "Michael Chen",
                    "job_title": "Senior Tech Lead",
                    "department": "Information Technology",
                    "match_score": 88,
                    "skills": ["Cloud Architecture", "Team Leadership", "System Design"]
                },
                {
                    "id": 2,
                    "name": "Sarah Chen",
                    "job_title": "Engineering Manager",
                    "department": "Information Technology",
                    "match_score": 85,
                    "skills": ["Project Management", "Agile Coaching", "Technical Strategy"]
                },
                {
                    "id": 3,
                    "name": "David Kumar",
                    "job_title": "Principal Engineer",
                    "department": "Information Technology",
                    "match_score": 82,
                    "skills": ["Architecture", "Performance Optimization", "Code Review"]
                }
            ]

            return {
                "Code": 200,
                "Message": "Success",
                "data": recommendations
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error getting mentor recommendations: {str(e)}"}
