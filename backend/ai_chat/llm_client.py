# backend/ai_chat/llm_client.py
from dotenv import load_dotenv; load_dotenv()

import os, json
import sys
from typing import Dict, List

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from shared.llm_clients import get_apim_client_for

# System prompts
SYSTEM_PROMPT = (
    "You are PORTalGPT, PSA's internal career co-pilot. "
    "Be concise, supportive, and specific. Prefer tool data over assumptions. "
    "If tool results are provided (plan, leadership, feedback), ground answers in them and avoid inventing numbers."
)
SYSTEM_COACH = (
    "You are PORTalGPT, PSA's internal career co-pilot. "
    "Default to a natural, conversational tone in 1–2 short paragraphs, with concrete, time-bound actions. "
    "Switch to concise bullets (<= 8) ONLY when the user explicitly asks for list/steps/roadmap/bullets. "
    "Always ground guidance in the provided plan and leadership signals; do not invent IDs or numbers."
)

MD_INSTRUCTIONS = (
    "Format the response strictly in GitHub-flavored Markdown. "
    "Use:\n"
    "## Snapshot\n"
    "- one sentence summary\n\n"
    "## What to Focus On (Top 3)\n"
    "- …\n- …\n- …\n\n"
    "## 30 / 60 / 90 Plan\n"
    "- **30d:** …\n- **60d:** …\n- **90d:** …\n\n"
    "## Suggested Courses\n"
    "- #<id> <title>\n\n"
    "## Mentor to Contact\n"
    "- <name>\n\n"
    "Keep numbers from the plan. No preamble, no code fences."
)

# APIM deployment names (from your .env); defaults match your earlier setup
CHAT_DEPLOY = os.getenv("AZURE_DEPLOY_GPT5_MINI", "gpt-5-mini")
EMBED_DEPLOY = os.getenv("AZURE_DEPLOY_EMBED", "text-embedding-3-small")  # not used here, but kept for completeness

# ---------- helpers ----------
def _safe(val, default):
    return default if val is None else val

def _fmt_pct(x):
    try:
        return f"{float(x):.1f}%"
    except Exception:
        return str(x)

# ---------- summary (for cards/panels) ----------
def summarize_plan_with_mock(plan: Dict, leadership: Dict) -> str:
    # Deterministic, safe fallback when LLM is unreachable
    target = plan.get("target_role", "a suitable next role")
    fit = _fmt_pct(plan.get("fit_score", 50))
    lines = [f"Target role: {target} (fit {fit})."]

    gaps = plan.get("missing_skills") or []
    if gaps:
        top = ', '.join(_safe(s.get('skill'), 'skill gap') for s in gaps[:3])
        lines.append(f"Top gaps: {top}.")

    courses = plan.get("recommended_courses") or []
    if courses:
        c1 = courses[0].get("title") or "a recommended course"
        lines.append(f"Start with course: {c1}.")

    mentors = plan.get("recommended_mentors") or []
    if mentors:
        m1 = mentors[0].get("name") or "a recommended mentor"
        lines.append(f"Suggested mentor: {m1}.")

    if leadership:
        lvl = leadership.get("level", "Developing")
        score = _fmt_pct(leadership.get("score", 50))
        lines.append(f"Leadership: {lvl} ({score}).")

    lines.append("Next 30/60/90 days: follow milestones in your plan.")
    return " ".join(lines)

def summarize(plan: Dict, leadership: Dict) -> str:
    content = json.dumps({"plan": plan, "leadership": leadership}, ensure_ascii=False)
    try:
        client = get_apim_client_for(CHAT_DEPLOY)
        resp = client.chat.completions.create(
            model=CHAT_DEPLOY,
            # ⚠️ REMOVE temperature (APIM blocks it)
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": "Summarize this structured plan in 6–8 crisp bullets with clear actions and reasons. Keep numbers as-is."},
                {"role": "user", "content": content},
            ],
        )
        return resp.choices[0].message.content
    except Exception:
        return summarize_plan_with_mock(plan, leadership)

# ---------- chat reply (for conversational UX) ----------
def _mock_reply(plan: Dict, leadership: Dict, user_message: str, history: str) -> str:
    # Simple deterministic fallback if APIM is unavailable
    role = plan.get("target_role", "a suitable next role")
    fit = plan.get("fit_score", 50)
    lead = leadership.get("level", "Developing")
    lower = (user_message or "").lower()
    if any(k in lower for k in ["list", "bullet", "steps", "roadmap"]):
        bullets = []
        gaps = plan.get("missing_skills") or []
        if gaps:
            bullets.append(f"Close top gap: {gaps[0].get('skill','a key skill')} in 30 days")
        course = (plan.get("recommended_courses") or [{}])[0].get("title")
        if course:
            bullets.append(f"Enroll: {course} this week")
        mentor = (plan.get("recommended_mentors") or [{}])[0].get("name")
        if mentor:
            bullets.append(f"Book mentor chat with {mentor} next week")
        bullets.append("Share progress update with manager in 4 weeks")
        return "\n".join(f"- {b}" for b in bullets[:8])
    # paragraphs
    return (
        f"You're tracking toward {role} (fit {fit}%). With leadership at {lead}, "
        "focus on one high-impact skill this month and apply it in a small project. "
        "Book one mentor conversation and schedule a progress check-in with your manager in 4 weeks."
    )

def llm_reply(plan: Dict, leadership: Dict, user_message: str, history_lines: List[str]) -> str:
    """Return a Markdown conversation reply grounded in plan+leadership.

    Style: default 1–2 short paragraphs; switch to bullets if the user asks.
    Uses APIM deployment without temperature.
    """
    history_text = "\n".join(history_lines[-6:]) if history_lines else ""

    # Derive highlights defensively
    target_role = plan.get("target_role")
    fit_score = plan.get("fit_score")
    gaps = plan.get("missing_skills") or []
    top_gap = (gaps[0].get("skill") if gaps else None)
    courses = plan.get("recommended_courses") or []
    course_title = (courses[0].get("title") if courses else None)
    mentors = plan.get("recommended_mentors") or []
    mentor_name = (mentors[0].get("name") if mentors else None)
    milestones = plan.get("milestones") or []
    milestone_focus = (milestones[0].get("focus") if milestones else None)
    lead_level = leadership.get("level") if isinstance(leadership, dict) else None
    lead_score = leadership.get("score") if isinstance(leadership, dict) else None

    tool_ctx = {
        "plan": plan,
        "leadership": leadership,
        "highlights": {
            "target_role": target_role,
            "fit_score": fit_score,
            "top_gap": top_gap,
            "course_title": course_title,
            "mentor_name": mentor_name,
            "milestone_focus": milestone_focus,
            "lead_level": lead_level,
            "lead_score": lead_score,
        },
        "history": history_text,
        "user_query": user_message,
    }

    lower = (user_message or "").lower()
    wants_bullets = any(k in lower for k in ["list", "bullet", "steps", "roadmap"])  # style hint

    # Compose instructions
    if wants_bullets:
        style = (
            "Return concise bullets (<= 8). Each bullet should be actionable and time-bound. "
            "Keep numbers from the plan; do not invent new ones."
        )
    else:
        style = (
            "Return 1–2 short paragraphs (no lists). Keep a friendly, concise tone with concrete, time-bound actions. "
            "Keep numbers from the plan; do not invent new ones."
        )

    try:
        client = get_apim_client_for(CHAT_DEPLOY)
        resp = client.chat.completions.create(
            model=CHAT_DEPLOY,
            messages=[
                {"role": "system", "content": SYSTEM_COACH},
                {"role": "user", "content": f"STYLE:\n{style}"},
                {"role": "user", "content": json.dumps(tool_ctx, ensure_ascii=False)},
            ],
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception:
        # Fallback: reuse summarize() which is grounded and safe
        return summarize(plan, leadership)