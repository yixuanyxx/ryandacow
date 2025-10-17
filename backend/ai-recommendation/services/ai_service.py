import sys
sys.path.append('..')
from repo.ai_repo import AIRepo
from typing import Dict, Any, Optional
from datetime import datetime, UTC

class AIService:
    def __init__(self, ai_repo: Optional[AIRepo] = None):
        self.ai_repo = ai_repo or AIRepo()
    
    def send_message(self, user_id: int, message: str) -> Dict[str, Any]:
        """Send message to AI and get response"""
        try:
            # Mock AI response - in real implementation would call OpenAI
            ai_response = f"Thank you for your message: '{message}'. This is a mock AI response for user {user_id}."
            
            return {
                "Code": 200,
                "Message": "AI response generated",
                "data": {
                    "ai_response": ai_response,
                    "suggestions": [],
                    "timestamp": datetime.now(UTC).isoformat()
                }
            }
        except Exception as e:
            return {
                "Code": 500,
                "Message": f"Error generating AI response: {str(e)}"
            }

    def get_quick_suggestions(self, user_id: int) -> Dict[str, Any]:
        """Get quick action suggestions for the user"""
        suggestions = [
            {
                "title": "Career Planning",
                "description": "Get personalized career advice",
                "action": "career_planning",
                "icon": "🎯"
            },
            {
                "title": "Skill Advice",
                "description": "Learn about skill development",
                "action": "skill_advice",
                "icon": "💡"
            },
            {
                "title": "Training Help",
                "description": "Find relevant training courses",
                "action": "training_help",
                "icon": "📚"
            },
            {
                "title": "Wellbeing Chat",
                "description": "Discuss work-life balance",
                "action": "wellbeing_chat",
                "icon": "🌱"
            }
        ]
        
        return {
            "Code": 200,
            "Message": "Success",
            "data": suggestions
        }
