import sys
sys.path.append('..')
from repo.user_repo import UserRepo
from typing import Dict, Any, Optional, List

class UserService:
    def __init__(self, user_repo: Optional[UserRepo] = None):
        self.user_repo = user_repo or UserRepo()
    
    def get_user_profile(self, user_id: str) -> dict:
        """Get complete user profile - MVP version with demo data"""
        try:
            # Demo user data - in production, this would come from database
            demo_users = {
                "EMP-20001": {
                    "id": "EMP-20001",
                    "email": "samantha.lee@globalpsa.com",
                    "name": "Samantha Lee",
                    "job_title": "Cloud Solutions Architect",
                    "department": "Information Technology",
                    "unit": "Infrastructure Architecture & Cloud",
                    "line_manager": "Victor Tan",
                    "in_role_since": "2022-07-01",
                    "hire_date": "2016-03-15",
                    "last_updated": "2025-10-09"
                },
                "EMP-20002": {
                    "id": "EMP-20002",
                    "email": "aisyah.rahman@globalpsa.com",
                    "name": "Nur Aisyah Binte Rahman",
                    "job_title": "Cybersecurity Analyst",
                    "department": "Information Technology",
                    "unit": "Cybersecurity Operations",
                    "line_manager": "Daniel Chua",
                    "in_role_since": "2024-07-01",
                    "hire_date": "2023-01-15",
                    "last_updated": "2025-10-09"
                },
                "EMP-20003": {
                    "id": "EMP-20003",
                    "email": "rohan.mehta@globalpsa.com",
                    "name": "Rohan Mehta",
                    "job_title": "Finance Manager (FP&A)",
                    "department": "Finance",
                    "unit": "Financial Planning & Analysis",
                    "line_manager": "Sarah Chen",
                    "in_role_since": "2023-01-01",
                    "hire_date": "2020-06-01",
                    "last_updated": "2025-10-09"
                },
                "EMP-20004": {
                    "id": "EMP-20004",
                    "email": "grace.lee@globalpsa.com",
                    "name": "Grace Lee",
                    "job_title": "Senior HR Business Partner",
                    "department": "Human Resource",
                    "unit": "Business Partnering",
                    "line_manager": "Michael Wong",
                    "in_role_since": "2021-03-01",
                    "hire_date": "2018-09-01",
                    "last_updated": "2025-10-09"
                },
                "EMP-20005": {
                    "id": "EMP-20005",
                    "email": "felicia.goh@globalpsa.com",
                    "name": "Felicia Goh",
                    "job_title": "Treasury Analyst",
                    "department": "Finance",
                    "unit": "Treasury Operations",
                    "line_manager": "David Lim",
                    "in_role_since": "2022-01-01",
                    "hire_date": "2019-08-01",
                    "last_updated": "2025-10-09"
                }
            }
            
            if user_id not in demo_users:
                return {"Code": 404, "Message": "User not found"}

            user_data = demo_users[user_id]
            
            # Demo skills data - in production, this would come from database
            demo_skills = {
                "EMP-20001": [
                    {
                        "id": 1,
                        "user_id": "EMP-20001",
                        "skill_id": 64,
                        "skills": {
                            "id": 64,
                            "function / unit / skill": "Info Tech: Infrastructure",
                            "specialisation / unit": "Cloud Computing: Cloud Architecture"
                        }
                    }
                ],
                "EMP-20002": [
                    {
                        "id": 2,
                        "user_id": "EMP-20002",
                        "skill_id": 65,
                        "skills": {
                            "id": 65,
                            "function / unit / skill": "Info Tech: Cybersecurity",
                            "specialisation / unit": "Cybersecurity Operations"
                        }
                    }
                ],
                "EMP-20003": [
                    {
                        "id": 3,
                        "user_id": "EMP-20003",
                        "skill_id": 45,
                        "skills": {
                            "id": 45,
                            "function / unit / skill": "Finance: Financial Planning & Analysis",
                            "specialisation / unit": "Financial Planning and Analysis"
                        }
                    }
                ],
                "EMP-20004": [
                    {
                        "id": 4,
                        "user_id": "EMP-20004",
                        "skill_id": 12,
                        "skills": {
                            "id": 12,
                            "function / unit / skill": "Human Resource: Business Partnering",
                            "specialisation / unit": "Generalist / Business Partner"
                        }
                    }
                ],
                "EMP-20005": [
                    {
                        "id": 5,
                        "user_id": "EMP-20005",
                        "skill_id": 48,
                        "skills": {
                            "id": 48,
                            "function / unit / skill": "Finance: Treasury Operations",
                            "specialisation / unit": "Treasury Management"
                        }
                    }
                ]
            }

            return {
                "Code": 200,
                "Message": "Success",
                "data": {
                    "user": user_data,
                    "skills": demo_skills.get(user_id, [])
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Internal server error: {str(e)}"}

    def get_users_by_department(self, department: str) -> dict:
        """Get users by department - MVP version with demo data"""
        try:
            # Demo users data
            all_users = {
                "EMP-20001": {
                    "id": "EMP-20001",
                    "email": "samantha.lee@globalpsa.com",
                    "name": "Samantha Lee",
                    "job_title": "Cloud Solutions Architect",
                    "department": "Information Technology",
                    "unit": "Infrastructure Architecture & Cloud",
                    "line_manager": "Victor Tan",
                    "in_role_since": "2022-07-01",
                    "hire_date": "2016-03-15",
                    "last_updated": "2025-10-09"
                },
                "EMP-20002": {
                    "id": "EMP-20002",
                    "email": "aisyah.rahman@globalpsa.com",
                    "name": "Nur Aisyah Binte Rahman",
                    "job_title": "Cybersecurity Analyst",
                    "department": "Information Technology",
                    "unit": "Cybersecurity Operations",
                    "line_manager": "Daniel Chua",
                    "in_role_since": "2024-07-01",
                    "hire_date": "2023-01-15",
                    "last_updated": "2025-10-09"
                },
                "EMP-20003": {
                    "id": "EMP-20003",
                    "email": "rohan.mehta@globalpsa.com",
                    "name": "Rohan Mehta",
                    "job_title": "Finance Manager (FP&A)",
                    "department": "Finance",
                    "unit": "Financial Planning & Analysis",
                    "line_manager": "Sarah Chen",
                    "in_role_since": "2023-01-01",
                    "hire_date": "2020-06-01",
                    "last_updated": "2025-10-09"
                },
                "EMP-20004": {
                    "id": "EMP-20004",
                    "email": "grace.lee@globalpsa.com",
                    "name": "Grace Lee",
                    "job_title": "Senior HR Business Partner",
                    "department": "Human Resource",
                    "unit": "Business Partnering",
                    "line_manager": "Michael Wong",
                    "in_role_since": "2021-03-01",
                    "hire_date": "2018-09-01",
                    "last_updated": "2025-10-09"
                },
                "EMP-20005": {
                    "id": "EMP-20005",
                    "email": "felicia.goh@globalpsa.com",
                    "name": "Felicia Goh",
                    "job_title": "Treasury Analyst",
                    "department": "Finance",
                    "unit": "Treasury Operations",
                    "line_manager": "David Lim",
                    "in_role_since": "2022-01-01",
                    "hire_date": "2019-08-01",
                    "last_updated": "2025-10-09"
                }
            }
            
            # Filter users by department
            department_users = [user for user in all_users.values() if user["department"] == department]
            
            return {
                "Code": 200,
                "Message": "Success",
                "data": department_users
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Internal server error: {str(e)}"}
