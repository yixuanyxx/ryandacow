import sys
sys.path.append('..')
from repo.recommendations_repo import RecommendationsRepo
from typing import Dict, Any, Optional, List
from datetime import datetime, UTC

class RecommendationsService:
    def __init__(self, repo: Optional[RecommendationsRepo] = None):
        self.repo = repo or RecommendationsRepo()
    
    def get_user_recommendations(self, user_id: int) -> Dict[str, Any]:
        """Get all recommendations for user dashboard"""
        try:
            user_profile = self.repo.get_user_profile(user_id)
            if not user_profile:
                return {"Code": 404, "Message": "User not found"}

            # Get different types of recommendations
            course_rec = self._get_top_course_recommendation(user_id)
            mentor_rec = self._get_top_mentor_recommendation(user_id)
            career_rec = self._get_career_recommendation(user_id)

            recommendations = []
            if course_rec:
                recommendations.append(course_rec)
            if mentor_rec:
                recommendations.append(mentor_rec)
            if career_rec:
                recommendations.append(career_rec)

            return {
                "Code": 200,
                "Message": "Success",
                "data": {
                    "recommendations": recommendations,
                    "user_name": f"{user_profile['first_name']} {user_profile['last_name']}",
                    "job_title": user_profile['job_title'],
                    "department": user_profile['department']
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error generating recommendations: {str(e)}"}

    def get_course_recommendations(self, user_id: int) -> Dict[str, Any]:
        """Get personalized course recommendations"""
        try:
            user_skills = self.repo.get_user_skills(user_id)
            courses = self.repo.get_courses()
            
            # Simple matching algorithm
            recommendations = []
            for course in courses[:3]:  # Top 3 courses
                match_score = self._calculate_course_match(user_skills, course)
                recommendations.append({
                    "id": course['id'],
                    "title": course['title'],
                    "description": course['description'],
                    "duration_hours": course['duration_hours'],
                    "difficulty_level": course['difficulty_level'],
                    "match_score": match_score,
                    "category": course['category']
                })

            # Sort by match score
            recommendations.sort(key=lambda x: x['match_score'], reverse=True)

            return {
                "Code": 200,
                "Message": "Success",
                "data": recommendations
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error getting course recommendations: {str(e)}"}

    def get_mentor_recommendations(self, user_id: int) -> Dict[str, Any]:
        """Get mentor recommendations"""
        try:
            user_skills = self.repo.get_user_skills(user_id)
            potential_mentors = self.repo.get_potential_mentors(user_id)
            
            recommendations = []
            for mentor in potential_mentors[:3]:  # Top 3 mentors
                mentor_skills = mentor.get('user_skills', [])
                match_score = self._calculate_mentor_match(user_skills, mentor_skills)
                
                recommendations.append({
                    "id": mentor['id'],
                    "name": f"{mentor['first_name']} {mentor['last_name']}",
                    "job_title": mentor['job_title'],
                    "department": mentor['department'],
                    "match_score": match_score,
                    "skills": [skill.get('skills', {}).get('name', '') for skill in mentor_skills[:3]]
                })

            # Sort by match score
            recommendations.sort(key=lambda x: x['match_score'], reverse=True)

            return {
                "Code": 200,
                "Message": "Success",
                "data": recommendations
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error getting mentor recommendations: {str(e)}"}

    def _get_top_course_recommendation(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get top course recommendation for dashboard"""
        courses = self.repo.get_courses()
        if not courses:
            return None

        # Return the first course as top recommendation
        course = courses[0]
        return {
            "type": "course",
            "title": course['title'],
            "description": course['description'],
            "match_score": 92,
            "metadata": {
                "duration_hours": course['duration_hours'],
                "difficulty_level": course['difficulty_level'],
                "category": course['category']
            }
        }

    def _get_top_mentor_recommendation(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get top mentor recommendation for dashboard"""
        potential_mentors = self.repo.get_potential_mentors(user_id)
        if not potential_mentors:
            return None

        # Return the first mentor as top recommendation
        mentor = potential_mentors[0]
        return {
            "type": "mentor",
            "title": f"{mentor['first_name']} {mentor['last_name']}",
            "description": f"{mentor['job_title']} with extensive experience",
            "match_score": 88,
            "metadata": {
                "job_title": mentor['job_title'],
                "department": mentor['department'],
                "experience_years": 15
            }
        }

    def _get_career_recommendation(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get career recommendation for dashboard"""
        pathways = self.repo.get_career_pathways()
        if not pathways:
            return None

        # Return the first pathway as recommendation
        pathway = pathways[0]
        return {
            "type": "career",
            "title": pathway['name'],
            "description": f"Next step: {pathway['name']} - {pathway['description']}",
            "match_score": 85,
            "metadata": {
                "department": pathway['department'],
                "level": pathway['level'],
                "skills_needed": ["Team Leadership", "System Design"]
            }
        }

    def _calculate_course_match(self, user_skills: List[Dict[str, Any]], course: Dict[str, Any]) -> float:
        """Calculate course match score"""
        # Simple matching - return high score for demo
        return 85.0 + (hash(course['title']) % 15)  # 85-100 range

    def _calculate_mentor_match(self, user_skills: List[Dict[str, Any]], mentor_skills: List[Dict[str, Any]]) -> float:
        """Calculate mentor match score"""
        # Simple matching - return high score for demo
        return 80.0 + (hash(str(mentor_skills)) % 20)  # 80-100 range
