import sys
sys.path.append('..')
from typing import Dict, Any, Optional, List
from datetime import datetime, UTC
import json
import os
from pathlib import Path
from shared.database import get_db_connection

class RecommendationsService:
    def __init__(self, repo: Optional[None] = None):
        self.db = get_db_connection()
        self.user_profiles = self._load_user_profiles()
    
    def _load_user_profiles(self) -> Dict[str, Any]:
        """Load user profiles from Employee_Profiles.json"""
        try:
            # Try multiple possible paths for the data directory
            possible_paths = [
                Path(__file__).parent / ".." / ".." / "data" / "Employee_Profiles.json",
                Path(__file__).parent / ".." / "data" / "Employee_Profiles.json",
                Path(__file__).parent / "data" / "Employee_Profiles.json",
                Path.cwd() / "data" / "Employee_Profiles.json",
                Path.cwd() / "backend" / "data" / "Employee_Profiles.json"
            ]
            
            for path in possible_paths:
                resolved_path = path.resolve()
                if resolved_path.exists():
                    with open(resolved_path, 'r') as f:
                        profiles = json.load(f)
                        # Convert list to dict for easier lookup
                        return {profile['employee_id']: profile for profile in profiles}
            
            print("Warning: Employee_Profiles.json not found, using empty profiles")
            return {}
        except Exception as e:
            print(f"Error loading user profiles: {e}")
            return {}
    
    def _get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile by employee ID"""
        return self.user_profiles.get(user_id)
    
    def _calculate_skill_match_score(self, user_skills: List[str], required_skills: List[str]) -> float:
        """Calculate match score based on skill overlap"""
        if not required_skills:
            return 0.0
        
        user_skill_set = set(skill.lower().strip() for skill in user_skills)
        required_skill_set = set(skill.lower().strip() for skill in required_skills)
        
        # Calculate overlap
        overlap = len(user_skill_set.intersection(required_skill_set))
        total_required = len(required_skill_set)
        
        # Base score from skill overlap
        skill_score = (overlap / total_required) * 100 if total_required > 0 else 0
        
        # Bonus for having more than 50% of required skills
        if overlap >= total_required * 0.5:
            skill_score += 10
        
        # Bonus for having all required skills
        if overlap == total_required:
            skill_score += 15
        
        return min(skill_score, 100)  # Cap at 100
    
    def _calculate_job_title_match_score(self, user_job_title: str, target_role: str) -> float:
        """Calculate match score based on job title similarity"""
        if not target_role:
            return 0.0
        
        user_title_lower = user_job_title.lower()
        target_role_lower = target_role.lower()
        
        # Direct match
        if user_title_lower == target_role_lower:
            return 100
        
        # Check for key terms
        user_keywords = set(user_title_lower.split())
        target_keywords = set(target_role_lower.split())
        
        overlap = len(user_keywords.intersection(target_keywords))
        total_keywords = len(target_keywords)
        
        if total_keywords == 0:
            return 0
        
        # Calculate similarity
        similarity = (overlap / total_keywords) * 100
        
        # Bonus for seniority progression (e.g., Manager -> Director)
        seniority_bonus = 0
        if 'manager' in user_title_lower and 'director' in target_role_lower:
            seniority_bonus = 20
        elif 'analyst' in user_title_lower and 'manager' in target_role_lower:
            seniority_bonus = 15
        elif 'architect' in user_title_lower and 'senior' in target_role_lower:
            seniority_bonus = 10
        
        return min(similarity + seniority_bonus, 100)
    
    def _find_best_course_matches(self, user_profile: Dict[str, Any], courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find best course matches for user"""
        if not courses or not user_profile:
            return []
        
        user_skills = [skill['skill_name'] for skill in user_profile.get('skills', [])]
        user_job_title = user_profile.get('employment_info', {}).get('job_title', '')
        
        scored_courses = []
        for course in courses:
            required_skills = course.get('required_skills', [])
            
            # Calculate skill match score
            skill_score = self._calculate_skill_match_score(user_skills, required_skills)
            
            # Calculate job title relevance score
            job_title_score = self._calculate_job_title_match_score(user_job_title, course.get('title', ''))
            
            # Combined score (weighted: 70% skills, 30% job title)
            combined_score = (skill_score * 0.7) + (job_title_score * 0.3)
            
            scored_courses.append({
                **course,
                'match_score': round(combined_score, 1),
                'skill_match_score': round(skill_score, 1),
                'job_title_score': round(job_title_score, 1)
            })
        
        # Sort by match score and return top matches
        scored_courses.sort(key=lambda x: x['match_score'], reverse=True)
        return scored_courses[:3]  # Return top 3 matches
    
    def _find_best_career_pathway_matches(self, user_profile: Dict[str, Any], career_pathways: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find best career pathway matches for user"""
        if not career_pathways or not user_profile:
            return []
        
        user_skills = [skill['skill_name'] for skill in user_profile.get('skills', [])]
        user_job_title = user_profile.get('employment_info', {}).get('job_title', '')
        
        scored_pathways = []
        for pathway in career_pathways:
            required_skills = pathway.get('required_skills', [])
            target_role = pathway.get('target_role', '')
            
            # Calculate skill match score
            skill_score = self._calculate_skill_match_score(user_skills, required_skills)
            
            # Calculate job title progression score
            job_title_score = self._calculate_job_title_match_score(user_job_title, target_role)
            
            # Combined score (weighted: 60% skills, 40% job title progression)
            combined_score = (skill_score * 0.6) + (job_title_score * 0.4)
            
            scored_pathways.append({
                **pathway,
                'match_score': round(combined_score, 1),
                'skill_match_score': round(skill_score, 1),
                'job_title_score': round(job_title_score, 1)
            })
        
        # Sort by match score and return top matches
        scored_pathways.sort(key=lambda x: x['match_score'], reverse=True)
        return scored_pathways[:2]  # Return top 2 matches
    
    def get_user_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get all recommendations for user dashboard"""
        try:
            # Get user profile for intelligent matching
            user_profile = self._get_user_profile(user_id)
            
            if not self.db.ready():
                return self._get_demo_recommendations(user_id)
            
            # Fetch real data from Supabase
            courses = self._fetch_courses()
            career_pathways = self._fetch_career_pathways()
            
            recommendations = []
            
            # Get intelligent course recommendations
            if courses and user_profile:
                best_courses = self._find_best_course_matches(user_profile, courses)
                for course in best_courses:
                    recommendations.append({
                        "type": "course",
                        "id": course["id"],
                        "title": course["title"],
                        "description": course["description"],
                        "match_score": course["match_score"],
                        "metadata": {
                            "duration_weeks": course["duration_weeks"],
                            "required_skills": course["required_skills"],
                            "category": "Professional Development",
                            "level": "Intermediate",
                            "skill_match_score": course["skill_match_score"],
                            "job_title_score": course["job_title_score"]
                        }
                    })
            elif courses:
                # Fallback to first course if no user profile
                course = courses[0]
                recommendations.append({
                    "type": "course",
                    "id": course["id"],
                    "title": course["title"],
                    "description": course["description"],
                    "match_score": 85,
                    "metadata": {
                        "duration_weeks": course["duration_weeks"],
                        "required_skills": course["required_skills"],
                        "category": "Professional Development",
                        "level": "Intermediate"
                    }
                })

            # Get intelligent career pathway recommendations
            if career_pathways and user_profile:
                best_pathways = self._find_best_career_pathway_matches(user_profile, career_pathways)
                for pathway in best_pathways:
                    recommendations.append({
                        "type": "career",
                        "id": pathway["id"],
                        "title": pathway["name"],
                        "description": pathway["description"],
                        "match_score": pathway["match_score"],
                        "metadata": {
                            "target_role": pathway["target_role"],
                            "required_skills": pathway["required_skills"],
                            "skill_match_score": pathway["skill_match_score"],
                            "job_title_score": pathway["job_title_score"]
                        }
                    })
            elif career_pathways:
                # Fallback to first pathway if no user profile
                pathway = career_pathways[0]
                recommendations.append({
                    "type": "career",
                    "id": pathway["id"],
                    "title": pathway["name"],
                    "description": pathway["description"],
                    "match_score": 80,
                    "metadata": {
                        "target_role": pathway["target_role"],
                        "required_skills": pathway["required_skills"]
                    }
                })

            # Add a demo mentor recommendation for now
            recommendations.append({
                "type": "mentor",
                "title": "Michael Chen",
                "description": "Senior Tech Lead with extensive experience in cloud architecture",
                "match_score": 88,
                "metadata": {
                    "job_title": "Senior Tech Lead",
                    "department": "Information Technology",
                    "experience_years": 15,
                    "skills": ["Cloud Architecture", "Team Leadership", "System Design"]
                }
            })

            return {
                "Code": 200,
                "Message": "Success",
                "data": {
                    "recommendations": recommendations
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error generating recommendations: {str(e)}"}

    def _fetch_courses(self) -> List[Dict[str, Any]]:
        """Fetch courses from Supabase"""
        try:
            response = self.db.client.table("courses").select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching courses: {e}")
            return []

    def _fetch_career_pathways(self) -> List[Dict[str, Any]]:
        """Fetch career pathways from Supabase"""
        try:
            response = self.db.client.table("career_pathways").select("*").execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching career pathways: {e}")
            return []

    def _get_demo_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Fallback to demo data if database is not available"""
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

    def get_course_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get personalized course recommendations"""
        try:
            if not self.db.ready():
                return self._get_demo_course_recommendations()
            
            # Fetch real courses from Supabase
            courses = self._fetch_courses()
            
            # Transform the data to match the expected format
            recommendations = []
            for course in courses:
                recommendations.append({
                    "id": course["id"],
                    "title": course["title"],
                    "description": course["description"],
                    "duration_weeks": course["duration_weeks"],
                    "match_score": 92,  # You can implement real matching logic here
                    "required_skills": course["required_skills"]
                })

            return {
                "Code": 200,
                "Message": "Success",
                "data": recommendations
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error getting course recommendations: {str(e)}"}

    def _get_demo_course_recommendations(self) -> Dict[str, Any]:
        """Fallback to demo course data if database is not available"""
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

    def get_career_pathway_recommendations(self, user_id: str) -> Dict[str, Any]:
        """Get career pathway recommendations"""
        try:
            if not self.db.ready():
                return self._get_demo_career_pathway_recommendations()
            
            # Fetch real career pathways from Supabase
            career_pathways = self._fetch_career_pathways()
            
            # Transform the data to match the expected format
            recommendations = []
            for pathway in career_pathways:
                recommendations.append({
                    "id": pathway["id"],
                    "name": pathway["name"],
                    "description": pathway["description"],
                    "target_role": pathway["target_role"],
                    "match_score": 88,  # You can implement real matching logic here
                    "required_skills": pathway["required_skills"]
                })

            return {
                "Code": 200,
                "Message": "Success",
                "data": recommendations
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Error getting career pathway recommendations: {str(e)}"}

    def _get_demo_career_pathway_recommendations(self) -> Dict[str, Any]:
        """Fallback to demo career pathway data if database is not available"""
        recommendations = [
            {
                "id": 1,
                "name": "Senior Software Engineer Path",
                "description": "Progression path to senior software engineering roles",
                "target_role": "Senior Software Engineer",
                "match_score": 88,
                "required_skills": ["System Design", "Team Leadership", "Technical Mentoring"]
            },
            {
                "id": 2,
                "name": "Cloud Solutions Architect Path",
                "description": "Progression path to cloud architecture roles",
                "target_role": "Cloud Solutions Architect",
                "match_score": 85,
                "required_skills": ["Cloud Architecture", "Infrastructure Design", "DevOps"]
            },
            {
                "id": 3,
                "name": "Engineering Manager Path",
                "description": "Progression path to engineering management roles",
                "target_role": "Engineering Manager",
                "match_score": 82,
                "required_skills": ["Project Management", "Team Leadership", "Strategic Planning"]
            }
        ]

        return {
            "Code": 200,
            "Message": "Success",
            "data": recommendations
        }

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
