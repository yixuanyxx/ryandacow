import sys
sys.path.append('..')
from repo.training_repo import TrainingRepo
from typing import Dict, Any, Optional
from datetime import datetime, UTC

class TrainingService:
    def __init__(self, training_repo: Optional[TrainingRepo] = None):
        self.training_repo = training_repo or TrainingRepo()
    
    def get_courses(self) -> Dict[str, Any]:
        """Get all available courses"""
        courses = self.training_repo.get_courses()
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": courses
        }

    def enroll_course(self, user_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Enroll user in a course"""
        required_fields = ['course_id']
        missing_fields = [field for field in required_fields if not payload.get(field)]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        enrollment_data = {
            'user_id': user_id,
            'course_id': payload['course_id'],
            'enrollment_date': datetime.now(UTC).isoformat(),
            'status': 'enrolled',
            'progress': 0.0
        }

        created_enrollment = self.training_repo.enroll_user(enrollment_data)
        
        return {
            "Code": 201,
            "Message": "Successfully enrolled in course",
            "data": created_enrollment
        }
