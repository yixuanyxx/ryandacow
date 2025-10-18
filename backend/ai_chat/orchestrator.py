import json
from typing import Dict
from backend.shared.leadership import leadership_score
from backend.recommendations.bootstrap_indices import load_roles, load_courses, load_mentors
from backend.shared.recommender import (
    role_recommendations, skill_gaps, top_courses_for_gaps, top_mentors, assemble_plan
)
from backend.ai_chat.llm_client import summarize

# Load in-memory indices once (fast, no DB needed)
ROLES   = load_roles()
COURSES = load_courses()
MENTORS = load_mentors()

# Minimal employee fetch. Replace with your real user/profile fetch when backend is ready.
def _get_employee_by_id_from_cache(cache_path: str, user_id: int) -> Dict:
    import json
    with open("backend/data/profile_cache.json","r",encoding="utf-8") as f:
        cache = json.load(f)
    entry = cache.get(str(user_id))
    if not entry:
        raise ValueError(f"user_id {user_id} not found in profile cache")
    entry["employee_id"] = str(user_id)
    return entry

def run_full_plan(user_id: int) -> Dict:
    # 1) employee profile (vector already precomputed in cache)
    employee = _get_employee_by_id_from_cache("backend/data/profile_cache.json", user_id)

    # 2) roles → best role
    role_hits = role_recommendations(employee, ROLES, top_k=5)
    if not role_hits:
        raise ValueError("No suitable roles found for this profile")
    best_hit = role_hits[0]
    target_role = next(r for r in ROLES if r["id"] == best_hit["role_id"])

    # 3) skill gaps
    gaps = skill_gaps(employee, target_role, top_k=6)

    # 4) courses & mentors
    courses = top_courses_for_gaps(gaps, COURSES, top_k=5)
    ments   = top_mentors(employee, MENTORS, top_k=3)

    # 5) assemble plan + get leadership readiness
    plan = assemble_plan(employee, best_hit, gaps, courses, ments)
    # — signals are mocked for now; replace when backend exposes real signals
    signals = {"training_completion": 0.55, "recognition_count": 2, "engagement": 0.7, "positive_feedback_ratio": 0.65}
    leader = leadership_score(signals)

    # 6) human-friendly summary
    summary = summarize(plan, leader)

    return {
        "plan": plan,
        "leadership": leader,
        "summary": summary,
        "alternatives": role_hits[1:3],  # show 2 more roles to compare
    }