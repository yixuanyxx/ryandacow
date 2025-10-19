# backend/ai_chat/orchestrator/orchestrator.py
from dotenv import load_dotenv; load_dotenv()

import os, json
from pathlib import Path
from typing import Dict

from backend.shared.leadership import leadership_score
from backend.recommendations.bootstrap_indices import load_roles, load_courses, load_mentors
from backend.shared.recommender import (
    role_recommendations, skill_gaps, top_courses_for_gaps, top_mentors, assemble_plan
)
from backend.ai_chat.llm_client import summarize

# --- data dir helper (works from anywhere; override with BACKEND_DATA_DIR) ---
def _data_dir() -> Path:
    env = os.getenv("BACKEND_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    # default: backend/data relative to this file
    return (Path(__file__).parent / ".." / ".." / "data").resolve()

PROFILE_CACHE = _data_dir() / "profile_cache.json"

# lazy-load indices once per process
_ROLES = _COURSES = _MENTORS = None
def _ensure_indices():
    global _ROLES, _COURSES, _MENTORS
    if _ROLES is None:
        _ROLES   = load_roles()
        _COURSES = load_courses()
        _MENTORS = load_mentors()

def _get_employee(user_id: int) -> Dict:
    with open(PROFILE_CACHE, "r", encoding="utf-8") as f:
        cache = json.load(f)
    entry = cache.get(str(user_id))
    if not entry:
        raise ValueError(f"user_id {user_id} not found in profile cache at {PROFILE_CACHE}")
    entry["employee_id"] = str(user_id)
    return entry

def run_full_plan(user_id: int) -> Dict:
    _ensure_indices()

    # 1) employee profile
    employee = _get_employee(user_id)

    # 2) roles → best role
    role_hits = role_recommendations(employee, _ROLES, top_k=5)
    if not role_hits:
        raise ValueError("No suitable roles found for this profile")
    best_hit = role_hits[0]
    target_role = next(r for r in _ROLES if r["id"] == best_hit["role_id"])

    # 3) gaps, 4) courses/mentors
    gaps    = skill_gaps(employee, target_role, top_k=6)
    courses = top_courses_for_gaps(gaps, _COURSES, top_k=5)
    ments   = top_mentors(employee, _MENTORS, top_k=3)

    # 5) plan + leadership
    plan   = assemble_plan(employee, best_hit, gaps, courses, ments)
    signals = {"training_completion": 0.55, "recognition_count": 2, "engagement": 0.7, "positive_feedback_ratio": 0.65}
    leader = leadership_score(signals)

    # 6) summary (LLM with safe fallback)
    try:
        summary = summarize(plan, leader)
    except Exception as e:
        summary = f"Summary unavailable ({e}). Target: {plan.get('target_role')} • Fit {plan.get('fit_score')}%"

    return {
        "plan": plan,
        "leadership": leader,
        "summary": summary,
        "alternatives": role_hits[1:3],
    }