import os, json
from typing import List, Dict

HAVE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are PORTalGPT, PSA's internal career co-pilot. "
    "Be concise, supportive, and specific. Prefer tool data over assumptions. "
    "If a tool result is provided, ground your answer in it and avoid inventing numbers."
)

def summarize_plan_with_mock(plan: Dict, leadership: Dict) -> str:
    # Deterministic, safe fallback when no OpenAI key is available.
    lines = []
    lines.append(f"Target role: {plan['target_role']} (fit {plan['fit_score']}%).")
    if plan.get("missing_skills"):
        top = ', '.join(s['skill'] for s in plan['missing_skills'][:3])
        lines.append(f"Top gaps: {top}.")
    if plan.get("recommended_courses"):
        c1 = plan['recommended_courses'][0]['title'] if plan['recommended_courses'] else None
        if c1: lines.append(f"Start with course: {c1}.")
    if plan.get("recommended_mentors"):
        m1 = plan['recommended_mentors'][0]['name']
        lines.append(f"Suggested mentor: {m1}.")
    if leadership:
        lines.append(f"Leadership: {leadership['level']} ({leadership['score']}%).")
    lines.append("Next 30/60/90 days: follow milestones in your plan.")
    return " ".join(lines)

def summarize_plan_with_llm(plan: Dict, leadership: Dict) -> str:
    # Late switch: wire OpenAI here when your key is ready.
    # Keep the shape the same so the rest of the app does not change.
    from openai import OpenAI
    client = OpenAI()
    content = json.dumps({"plan": plan, "leadership": leadership}, ensure_ascii=False)
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        temperature=0.3,
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user","content":"Summarize this structured plan for the employee in 6-8 bullet points with clear actions and reasons. Keep numbers as-is."},
            {"role":"user","content":content}
        ],
    )
    return resp.choices[0].message.content

def summarize(plan: Dict, leadership: Dict) -> str:
    if HAVE_OPENAI:
        try:
            return summarize_plan_with_llm(plan, leadership)
        except Exception:
            # Hard fallback if API hiccups
            return summarize_plan_with_mock(plan, leadership)
    else:
        return summarize_plan_with_mock(plan, leadership)