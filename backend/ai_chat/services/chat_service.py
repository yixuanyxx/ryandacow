import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from typing import Dict, Any, Optional
from datetime import datetime, UTC
import traceback
from repo.chat_repo import ChatRepo
from orchestrator.orchestrator import run_full_plan
from llm_client import summarize, llm_reply

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

    def generate_career_guidance(self, user_id: int, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 1) Core plan
            result       = run_full_plan(user_id)
            plan         = result.get("plan") or {}
            leadership   = result.get("leadership") or {}
            summary      = result.get("summary") or "Here’s a personalized plan."
            alternatives = result.get("alternatives") or []

            # 2) Feedback scaffold
            missing     = plan.get("missing_skills") or []
            top_courses = plan.get("recommended_courses") or []
            top_mentors = plan.get("recommended_mentors") or []
            strengths   = plan.get("skills") or []

            growth_areas = [m.get("skill", "Skill gap") for m in missing[:3]]
            rec_actions  = []
            if top_courses: rec_actions.append(f"Start {top_courses[0].get('title','a recommended course')}")
            if top_mentors: rec_actions.append(f"Schedule a mentor chat with {top_mentors[0].get('name','a recommended mentor')}")
            rec_actions.append("Set two measurable goals for the next 30 days")

            lead_level = leadership.get("level", "Developing")
            lead_score = leadership.get("score", 50)
            dev_plan   = leadership.get("development_plan") or []
            lead_focus = ", ".join(d.get("skill","a focus area") for d in dev_plan[:2]) or "core leadership behaviors"

            feedback = {
                "strengths": strengths[:3],
                "growth_areas": growth_areas,
                "recommended_actions": rec_actions,
                "leadership_feedback": {
                    "level": lead_level,
                    "score": lead_score,
                    "comment": f"Focus on {lead_focus} to progress from '{lead_level}'."
                }
            }

            # 3) Short convo history (best-effort)
            try:
                get_ctx = getattr(self.chat_repo, "get_session_messages_for_context", None)
                if callable(get_ctx):
                    msgs = get_ctx(user_id, limit=6)
                else:
                    sess = self.chat_repo.get_user_session(user_id)
                    msgs = self.chat_repo.get_session_messages(sess['id'])[-6:] if sess else []
            except Exception:
                msgs = []
            history_lines = [f"{m['role']}: {m['content']}" for m in msgs]

            # 4) Conversational reply (fallback to summary on error)
            try:
                reply_md = llm_reply(plan, leadership, message, history_lines) or summary
            except Exception:
                reply_md = summary

            # 5) Tiny extras for the right panel
            plan["top_gaps"] = [m.get("skill") for m in (plan.get("missing_skills") or [])][:3]
            plan["kpis"] = {
                "fit_score": plan.get("fit_score", 0),
                "primary_gap_pct": (plan.get("missing_skills", [{"gap_score": 0}])[0].get("gap_score", 0)),
                "courses_count": len(top_courses),
            }
            next_questions = [
                "Give me a 2-week micro-plan for the top gap",
                "Draft a DM to request a 1:1 with the suggested mentor",
                "Suggest an internal project to apply these skills",
            ]
            grounding = {
                "course_ids": [c.get("id") for c in top_courses],
                "mentor_ids": [m.get("id") for m in top_mentors],
                "target_role": plan.get("target_role"),
            }

            # 6) Return unified payload (what the frontend expects)
            return {
                "Code": 200,
                "Message": "AI guidance generated",
                "data": {
                    "reply": reply_md,          # ← show this in chat bubble
                    "summary": summary,         # ← still available for cards
                    "plan": plan,
                    "leadership": leadership,
                    "alternatives": alternatives,
                    "feedback": {**feedback, "next_questions": next_questions},
                    "grounding": grounding,
                },
            }

        except Exception as e:
            traceback.print_exc()
            return {"Code": 500, "Message": f"Guidance pipeline error: {e}"}

    def _generate_ai_response(self, user_id: int, message: str, context: Dict[str, Any]) -> str:
        # 1) gather short convo snippet (kept — with the safety block from B)
        try:
            get_ctx = getattr(self.chat_repo, "get_session_messages_for_context", None)
            if callable(get_ctx):
                messages = get_ctx(user_id, limit=6)
            else:
                sess = self.chat_repo.get_user_session(user_id)
                messages = self.chat_repo.get_session_messages(sess['id'])[-6:] if sess else []
        except Exception:
            messages = []

        conversation_snippet = "\n".join(f"{m['role'].capitalize()}: {m['content']}" for m in messages)

        # 2) run your orchestrator (deterministic plan + leadership)
        result = run_full_plan(user_id)

        # 3) tone prompt (optional context for future upgrades)
        user_profile = context.get("user_profile", {})
        persona = user_profile.get("job_title", "professional")
        _ = (
            f"You are PORTalGPT, PSA's internal career mentor.\n"
            f"User role: {persona}\n"
            f"Recent conversation:\n{conversation_snippet}\n"
        )

        # 4) ✅ robust summary (uses OpenAI if configured, else mock)
        return summarize(result["plan"], result["leadership"])