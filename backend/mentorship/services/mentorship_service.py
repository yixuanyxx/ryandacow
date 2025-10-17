import sys
sys.path.append('..')
from repo.mentorship_repo import MentorshipRepo
from typing import Dict, Any, Optional
from datetime import datetime, UTC

class MentorshipService:
    def __init__(self, mentorship_repo: Optional[MentorshipRepo] = None):
        self.mentorship_repo = mentorship_repo or MentorshipRepo()
    
    def find_mentors(self, user_id: int) -> Dict[str, Any]:
        """Find potential mentors based on skills and experience"""
        # Mock implementation - in real version would match based on skills
        mentors = [
            {
                "id": 1,
                "name": "John Smith",
                "department": "Engineering",
                               "skills": ["Python", "Leadership", "Mentoring"],
                "match_score": 0.85
            },
            {
                "id": 2,
                "name": "Sarah Johnson",
                "department": "Product Management",
                "skills": ["Strategy", "Communication", "Leadership"],
                "match_score": 0.78
            }
        ]
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": mentors
        }

    def send_mentorship_request(self, mentee_id: int, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send mentorship request"""
        required_fields = ['mentor_id', 'message']
        missing_fields = [field for field in required_fields if not payload.get(field)]
        
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        request_data = {
            'mentee_id': mentee_id,
            'mentor_id': payload['mentor_id'],
            'message': payload['message'],
            'status': 'pending',
            'created_at': datetime.now(UTC).isoformat(),
            'updated_at': datetime.now(UTC).isoformat()
        }

        created_request = self.mentorship_repo.create_request(request_data)
        
        return {
            "Code": 201,
            "Message": "Mentorship request sent successfully",
            "data": created_request
        }
