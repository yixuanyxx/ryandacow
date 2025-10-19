import sys
sys.path.append('..')
from shared.auth import generate_token
from typing import Dict, Any, Optional

class AuthService:
    def __init__(self, auth_repo: Optional[None] = None):
        # For MVP, we don't use the database repo
        pass
    
    def login_user(self, email: str, password: str) -> dict:
        """Login user with demo credentials - MVP version"""
        try:
            # Demo user data - in production, this would come from database
            demo_users = {
                "samantha.lee@globalpsa.com": {
                    "id": "EMP-20001",
                    "email": "samantha.lee@globalpsa.com",
                    "name": "Samantha Lee",
                    "job_title": "Cloud Solutions Architect",
                    "department": "Information Technology",
                    "unit": "Cloud Infrastructure",
                    "line_manager": "Michael Chen"
                },
                "aisyah.rahman@globalpsa.com": {
                    "id": "EMP-20002",
                    "email": "aisyah.rahman@globalpsa.com",
                    "name": "Aisyah Rahman",
                    "job_title": "Cybersecurity Analyst",
                    "department": "Information Technology",
                    "unit": "Security Operations",
                    "line_manager": "David Kumar"
                },
                "rohan.mehta@globalpsa.com": {
                    "id": "EMP-20003",
                    "email": "rohan.mehta@globalpsa.com",
                    "name": "Rohan Mehta",
                    "job_title": "Finance Manager (FP&A)",
                    "department": "Finance",
                    "unit": "Financial Planning & Analysis",
                    "line_manager": "Sarah Chen"
                },
                "grace.lee@globalpsa.com": {
                    "id": "EMP-20004",
                    "email": "grace.lee@globalpsa.com",
                    "name": "Grace Lee",
                    "job_title": "Senior HR Business Partner",
                    "department": "Human Resource",
                    "unit": "Business Partnering",
                    "line_manager": "Michael Wong"
                },
                "felicia.goh@globalpsa.com": {
                    "id": "EMP-20005",
                    "email": "felicia.goh@globalpsa.com",
                    "name": "Felicia Goh",
                    "job_title": "Treasury Analyst",
                    "department": "Finance",
                    "unit": "Treasury Operations",
                    "line_manager": "David Lim"
                }
            }
            
            # Check if email exists in demo users
            if email not in demo_users:
                return {"Code": 401, "Message": "Invalid email or password"}

            # For MVP, check if password matches demo password
            if password != 'demo123':
                return {"Code": 401, "Message": "Invalid email or password"}

            user_data = demo_users[email]
            
            # Generate token using user ID (which is the employee ID in your case)
            token = generate_token(user_data['id'])

            return {
                "Code": 200,
                "Message": "Login successful",
                "data": {
                    "user": {
                        "id": user_data['id'],
                        "email": user_data['email'],
                        "name": user_data['name'],
                        "job_title": user_data['job_title'],
                        "department": user_data['department'],
                        "unit": user_data['unit'],
                        "line_manager": user_data['line_manager']
                    },
                    "token": token
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Internal server error: {str(e)}"}

    def get_user_profile(self, user_id: str) -> dict:
        """Get complete user profile - MVP version"""
        try:
            # Demo user data - in production, this would come from database
            demo_users = {
                "EMP-20001": {
                    "id": "EMP-20001",
                    "email": "samantha.lee@globalpsa.com",
                    "name": "Samantha Lee",
                    "job_title": "Cloud Solutions Architect",
                    "department": "Information Technology",
                    "unit": "Cloud Infrastructure",
                    "line_manager": "Michael Chen",
                    "in_role_since": "2022-03-01",
                    "hire_date": "2020-06-01",
                    "last_updated": "2025-10-09"
                },
                "EMP-20002": {
                    "id": "EMP-20002",
                    "email": "aisyah.rahman@globalpsa.com",
                    "name": "Aisyah Rahman",
                    "job_title": "Cybersecurity Analyst",
                    "department": "Information Technology",
                    "unit": "Security Operations",
                    "line_manager": "David Kumar",
                    "in_role_since": "2021-08-01",
                    "hire_date": "2019-03-01",
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
                            "function / unit / skill": "Info Tech: Security",
                            "specialisation / unit": "Cybersecurity: Threat Analysis"
                        }
                    }
                ],
                "EMP-20003": [
                    {
                        "id": 3,
                        "user_id": "EMP-20003",
                        "skill_id": 66,
                        "skills": {
                            "id": 66,
                            "function / unit / skill": "Finance: Analysis",
                            "specialisation / unit": "Financial Planning: Budget Management"
                        }
                    }
                ],
                "EMP-20004": [
                    {
                        "id": 4,
                        "user_id": "EMP-20004",
                        "skill_id": 67,
                        "skills": {
                            "id": 67,
                            "function / unit / skill": "HR: Business Partnering",
                            "specialisation / unit": "Talent Management: Employee Relations"
                        }
                    }
                ],
                "EMP-20005": [
                    {
                        "id": 5,
                        "user_id": "EMP-20005",
                        "skill_id": 68,
                        "skills": {
                            "id": 68,
                            "function / unit / skill": "Finance: Treasury",
                            "specialisation / unit": "Cash Management: Risk Assessment"
                        }
                    }
                ]
            }

            return {
                "Code": 200,
                "Message": "Success",
                "data": {
                    "user": {
                        "id": user_data['id'],
                        "email": user_data['email'],
                        "name": user_data['name'],
                        "job_title": user_data['job_title'],
                        "department": user_data['department'],
                        "unit": user_data['unit'],
                        "line_manager": user_data['line_manager'],
                        "in_role_since": user_data['in_role_since'],
                        "hire_date": user_data['hire_date'],
                        "last_updated": user_data['last_updated']
                    },
                    "skills": demo_skills.get(user_id, [])
                }
            }
        except Exception as e:
            return {"Code": 500, "Message": f"Internal server error: {str(e)}"}