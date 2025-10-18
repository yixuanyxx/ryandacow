import sys
sys.path.append('..')
from repo.chat_repo import ChatRepo
from typing import Dict, Any, Optional
from datetime import datetime, UTC
import os

class ChatService:
    def __init__(self, chat_repo: Optional[ChatRepo] = None):
        self.chat_repo = chat_repo or ChatRepo()
    
    def send_message(self, user_id: int, message: str) -> Dict[str, Any]:
        """Send message to AI and get response"""
        try:
            # Get or create chat session
            session = self.chat_repo.get_user_session(user_id)
            if not session:
                session = self.chat_repo.create_session({
                    'user_id': user_id,
                    'session_name': 'Career Chat',
                    'context_data': self._get_user_context(user_id),
                    'created_at': datetime.now(UTC).isoformat()
                })

            # Save user message
            self.chat_repo.create_message({
                'session_id': session['id'],
                'role': 'user',
                'content': message,
                'created_at': datetime.now(UTC).isoformat()
            })

            # Generate AI response
            ai_response = self._generate_ai_response(user_id, message, session['context_data'])

            # Save AI response
            self.chat_repo.create_message({
                'session_id': session['id'],
                'role': 'assistant',
                'content': ai_response,
                'created_at': datetime.now(UTC).isoformat()
            })

            return {
                "Code": 200,
                "Message": "AI response generated",
                "data": {
                    "ai_response": ai_response,
                    "timestamp": datetime.now(UTC).isoformat()
                }
            }
        except Exception as e:
            return {
                "Code": 500,
                "Message": f"Error generating AI response: {str(e)}"
            }

    def get_chat_history(self, user_id: int) -> Dict[str, Any]:
        """Get chat history for user"""
        session = self.chat_repo.get_user_session(user_id)
        if not session:
            return {
                "Code": 200,
                "Message": "No chat history found",
                "data": {"messages": []}
            }

        messages = self.chat_repo.get_session_messages(session['id'])
        return {
            "Code": 200,
            "Message": "Success",
            "data": {"messages": messages}
        }

    def clear_chat(self, user_id: int) -> Dict[str, Any]:
        """Clear chat history for user"""
        session = self.chat_repo.get_user_session(user_id)
        if session:
            # Delete messages
            self.chat_repo.db.table("ai_chat_messages").delete().eq("session_id", session['id']).execute()
            # Delete session
            self.chat_repo.db.table("ai_chat_sessions").delete().eq("id", session['id']).execute()

        return {
            "Code": 200,
            "Message": "Chat history cleared"
        }

    def _get_user_context(self, user_id: int) -> Dict[str, Any]:
        """Get user context for AI"""
        user_profile = self.chat_repo.get_user_profile(user_id)
        user_skills = self.chat_repo.get_user_skills(user_id)
        
        return {
            "user_profile": user_profile,
            "user_skills": user_skills
        }

    def _generate_ai_response(self, user_id: int, message: str, context: Dict[str, Any]) -> str:
        """Generate AI response - MVP version with predefined responses"""
        
        # Get user context
        user_profile = context.get('user_profile', {})
        user_skills = context.get('user_skills', [])
        
        user_name = user_profile.get('first_name', 'there')
        job_title = user_profile.get('job_title', 'employee')
        department = user_profile.get('department', 'your department')
        
        # Extract skills for context
        skill_names = [skill.get('skills', {}).get('name', '') for skill in user_skills if skill.get('skills')]
        
        # Predefined responses based on common questions
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['skill', 'skills', 'learn', 'develop']):
            if 'tech lead' in message_lower or 'lead' in message_lower:
                return f"""Hi {user_name}! Based on your profile as a {job_title} in {department}, here are the key skills you need to become a Tech Lead:

**High Priority Skills:**
• Team Leadership - Lead and mentor development teams
• System Architecture - Design scalable system architectures  
• Agile Coaching - Guide teams in agile methodologies

**Medium Priority Skills:**
• Project Management - Plan and execute technical projects
• Communication - Present technical concepts to stakeholders

I recommend starting with our "Leadership Fundamentals" course to build your team leadership skills. Would you like me to suggest specific training courses for any of these areas?"""

            elif 'course' in message_lower or 'training' in message_lower:
                return f"""Great question, {user_name}! Based on your current skills in {', '.join(skill_names[:3]) if skill_names else 'your field'}, I recommend these courses:

**For your career growth:**
• Advanced Python for Leaders (40 hours) - Builds on your Python skills
• System Design Masterclass (32 hours) - Essential for senior roles
• Leadership Fundamentals (24 hours) - Develops management skills

**Next Steps:**
1. Start with Leadership Fundamentals to build soft skills
2. Take System Design Masterclass for technical depth
3. Consider Advanced Python for Leaders for specialization

Would you like more details about any of these courses?"""

            else:
                return f"""Hi {user_name}! I'd be happy to help you with skill development. 

Based on your role as a {job_title}, here are some areas to focus on:

**Technical Skills:**
• Advanced programming languages
• System design and architecture
• Cloud computing platforms

**Leadership Skills:**
• Team management
• Project planning
• Communication and presentation

What specific skills are you most interested in developing? I can provide personalized recommendations based on your career goals."""

        elif any(word in message_lower for word in ['mentor', 'mentorship', 'advice', 'guidance']):
            return f"""Hi {user_name}! Mentorship is a great way to accelerate your career growth.

**Finding a Mentor:**
• Look for senior professionals in {department}
• Seek someone with 5+ years more experience than you
• Consider both technical and leadership mentors

**What to Look For:**
• Experience in roles you aspire to
• Strong communication skills
• Willingness to share knowledge

**How to Approach:**
• Be specific about what you want to learn
• Show genuine interest in their expertise
• Offer to help with their projects too

Would you like me to suggest potential mentors based on your career goals?"""

        elif any(word in message_lower for word in ['career', 'path', 'goal', 'next step']):
            return f"""Hi {user_name}! Let's discuss your career path.

**Your Current Position:** {job_title} in {department}

**Potential Next Steps:**
• Senior {job_title} - Deepen technical expertise
• Tech Lead - Lead technical teams
• Engineering Manager - Manage teams and projects

**Recommended Path:** Based on your skills, I suggest aiming for Tech Lead in 2-3 years.

**Action Plan:**
1. Develop leadership skills through courses
2. Take on mentoring opportunities
3. Lead technical projects
4. Build system design expertise

What specific role interests you most? I can create a detailed development plan."""

        else:
            return f"""Hi {user_name}! I'm here to help with your career development at PSA.

I can assist you with:
• **Skill Development** - Recommend courses and learning paths
• **Career Planning** - Help you set and achieve career goals  
• **Mentorship** - Connect you with potential mentors
• **Training** - Suggest relevant courses and certifications

What would you like to work on today? Feel free to ask me about:
- Skills you need for your next role
- Training courses that match your goals
- Career advancement strategies
- Finding mentors in your field

How can I help you grow professionally?"""
