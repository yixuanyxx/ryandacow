# backend/ai_chat/llm_client.py
from dotenv import load_dotenv; load_dotenv()

import os, json
from typing import Dict, List
from backend.shared.llm_clients import get_apim_client_for

SYSTEM_PROMPT = (
    "You are PORTalGPT, PSA's internal career co-pilot. "
    "Be concise, supportive, and specific. Prefer tool data over assumptions. "
    "If tool results are provided (plan, leadership, feedback), ground answers in them and avoid inventing numbers."
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
    # Varies by user_message so it doesn’t look identical
    role = plan.get("target_role", "a suitable next role")
    fit = plan.get("fit_score", 50)
    lead = leadership.get("level", "Developing")
    lower = (user_message or "").lower()
    if "mentor" in lower:
        return (
            f"Good idea. For your target {role} (fit {fit:.1f}%) and leadership level {lead}, "
            "book one mentor chat this week. I can suggest a mentor and a 3-question agenda if you’d like."
        )
    if "course" in lower or "learn" in lower:
        c1 = (plan.get("recommended_courses") or [{}])[0].get("title", "the top recommended course")
        return (
            f"For your target {role} (fit {fit:.1f}%), start with {c1}. "
            "Apply it in a small project within 2–3 weeks, then share results with your manager."
        )
    if "skills" in lower or "gap" in lower:
        gaps = plan.get("missing_skills") or []
        top = ", ".join(g.get("skill", "a gap") for g in gaps[:2]) or "your top gap areas"
        return (
            f"Top skill gaps: {top}. Focus the next 30 days on closing one gap. "
            "I can break this into weekly actions if you say 'weekly plan'."
        )
    return (
        f"For your target {role} (fit {fit:.1f}%) and leadership level {lead}, "
        "focus on the first milestone this month. Want me to break it into weekly actions?"
    )

def llm_reply(plan: Dict, leadership: Dict, user_message: str, history_lines: List[str]) -> str:
    """Return a Markdown conversation reply grounded in plan+leadership."""
    content = json.dumps({"plan": plan, "leadership": leadership}, ensure_ascii=False)
    history_text = "\n".join(history_lines[-6:]) if history_lines else ""
    system = (
        "You are PORTalGPT, PSA's internal career co-pilot. "
        "Be supportive, specific, and grounded in the provided plan JSON. "
        "Do not invent IDs, numbers, or entities."
    )
    user = (
        f"User message:\n{user_message}\n\n"
        f"Recent conversation (if any):\n{history_text}\n\n"
        f"Structured plan JSON:\n{content}\n\n{MD_INSTRUCTIONS}"
    )
    try:
        client = get_apim_client_for(CHAT_DEPLOY)
        resp = client.chat.completions.create(
            model=CHAT_DEPLOY,  # deployment name
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # Fallback: quick plain text made from plan
        lines = [
            f"## Snapshot\n- Target: {plan.get('target_role')} (fit {plan.get('fit_score')}%)",
            "## What to Focus On (Top 3)",
        ]
        for g in (plan.get("missing_skills") or [])[:3]:
            lines.append(f"- {g.get('skill')}")
        lines += [
            "## 30 / 60 / 90 Plan",
            "- **30d:** Enroll in course #1 and meet a mentor",
            "- **60d:** Apply skills in a project",
            "- **90d:** Present outcomes to manager",
        ]
        return "\n".join(lines)