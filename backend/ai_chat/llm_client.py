# backend/ai_chat/llm_client.py
from dotenv import load_dotenv; load_dotenv()

import os, json
from typing import Dict
from backend.shared.llm_clients import get_apim_client_for

SYSTEM_PROMPT = (
    "You are PORTalGPT, PSA's internal career co-pilot. "
    "Be concise, supportive, and specific. Prefer tool data over assumptions. "
    "If a tool result is provided, ground your answer in it and avoid inventing numbers."
)

# Use the APIM deployment for chat (gpt-5-mini by default)
CHAT_DEPLOY = os.getenv("AZURE_DEPLOY_GPT5_MINI", "gpt-5-mini")

def summarize_plan_with_mock(plan: Dict, leadership: Dict) -> str:
    # Deterministic, safe fallback when LLM is unreachable
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

def summarize(plan: Dict, leadership: Dict) -> str:
    """
    Preferred path: use APIM (deployment-scoped base URL + `api-key` header).
    Falls back to a deterministic mock if the gateway errors.
    """
    content = json.dumps({"plan": plan, "leadership": leadership}, ensure_ascii=False)
    try:
        client = get_apim_client_for(CHAT_DEPLOY)
        resp = client.chat.completions.create(
            model=CHAT_DEPLOY,          # APIM expects deployment name here
            temperature=0.3,
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":"Summarize this structured plan in 6–8 crisp bullets with clear actions and reasons. Keep numbers as-is."},
                {"role":"user","content":content}
            ],
        )
        return resp.choices[0].message.content
    except Exception:
        return summarize_plan_with_mock(plan, leadership)