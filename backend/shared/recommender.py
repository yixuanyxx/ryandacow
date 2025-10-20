# backend/shared/recommender.py

import numpy as np
import sys
import os
from typing import Dict, List

# Add the current directory to the path so we can import from shared modules
sys.path.append(os.path.dirname(__file__))

from embeddings import embed_text, cosine
from skill_normalizer import normalize_list

# --- Helper to convert lists to numpy arrays ---
def _as_np(v): 
    return np.array(v, dtype=float)


# =====================================================
# 1️⃣ ROLE RECOMMENDATION
# =====================================================
def role_recommendations(employee: dict, roles: list, top_k: int = 5) -> list:
    """
    Always return top_k best matches (no hard min threshold).
    Include the final score so upstream can sort or display.
    """
    from embeddings import embed_text, cosine

    # build query text from richer signals
    q = " ".join([
        employee.get("job_title",""),
        " ".join(employee.get("top_skills", [])[:8]),
        " ".join([p.get("title","") for p in employee.get("projects", [])[:3]])
    ]).strip() or employee.get("job_title","")
    qv = embed_text(q)

    scored = []
    for r in roles:
        # concat role text
        rtxt = " ".join(filter(None, [
            r.get("role",""),
            " ".join(r.get("skills", [])[:10]),
            r.get("summary","")
        ]))
        rv = r.get("vector") or embed_text(rtxt)  # if you stored vectors, use them; else embed on the fly
        s = cosine(qv, rv)
        scored.append({"role_id": r["id"], "role": r.get("role",""), "score": float(s)})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


# =====================================================
# 2️⃣ SKILL GAP ANALYSIS
# =====================================================
def skill_gaps(employee: Dict, target_role: Dict, top_k: int = 6) -> List[Dict]:
    """
    Compare an employee’s overall vector with each required skill vector of a role.
    Return the skills farthest from the employee (biggest gaps).
    """
    e_vec = _as_np(employee["vector"])
    reqs = normalize_list(target_role.get("required_skills", []))

    gaps = []
    for skill in reqs:
        s_vec = embed_text(skill)
        gap_score = (1 - cosine(e_vec, s_vec)) * 100
        gaps.append({"skill": skill, "gap_score": round(gap_score, 1)})

    # Sort by largest gap first
    return sorted(gaps, key=lambda x: x["gap_score"], reverse=True)[:top_k]


# =====================================================
# 3️⃣ COURSE MATCHING
# =====================================================
def top_courses_for_gaps(gaps: List[Dict], course_index: List[Dict], top_k: int = 5) -> List[Dict]:
    """
    Find courses whose required_skills overlap with the employee's biggest gaps.
    """
    needed = set(g["skill"].lower() for g in gaps[:4])
    scored = []

    for c in course_index:
        tags = set(normalize_list(c.get("required_skills", [])))
        overlap = len(needed.intersection(tags)) / max(1, len(needed))
        scored.append({**c, "match_score": round(100 * overlap, 1)})

    return sorted(scored, key=lambda x: x["match_score"], reverse=True)[:top_k]


# =====================================================
# 4️⃣ MENTOR MATCHING
# =====================================================
def top_mentors(employee: Dict, mentor_index: List[Dict], top_k: int = 3) -> List[Dict]:
    """
    Rank mentors by vector similarity to the employee.
    """
    e_vec = _as_np(employee["vector"])
    ranked = []

    for m in mentor_index:
        sim = cosine(e_vec, _as_np(m["vector"]))
        ranked.append({**m, "match_score": round(100 * sim, 1)})

    return sorted(ranked, key=lambda x: x["match_score"], reverse=True)[:top_k]


# =====================================================
# 5️⃣ PLAN ASSEMBLER
# =====================================================
def assemble_plan(employee: Dict, role_hit: Dict,
                  gaps: List[Dict], courses: List[Dict],
                  mentors: List[Dict]) -> Dict:
    """
    Bundle all recommendations into one structured career plan object.
    """
    plan = {
        "employee_id": employee["employee_id"],
        "target_role": role_hit["role"],
        "fit_score": role_hit["score"],
        "missing_skills": gaps,
        "recommended_courses": [
            {"id": c["id"], "title": c["title"], "match": c["match_score"]}
            for c in courses
        ],
        "recommended_mentors": [
            {"id": m["id"], "name": m["name"], "match": m["match_score"]}
            for m in mentors
        ],
        "milestones": [
            {
                "phase": "30 days",
                "focus": "Close top 2 skill gaps",
                "actions": [
                    "Enroll in recommended course #1",
                    "Complete 1:1 mentor session"
                ],
            },
            {
                "phase": "60 days",
                "focus": "Apply skills in project context",
                "actions": ["Volunteer for stretch task", "Update learning log"],
            },
            {
                "phase": "90 days",
                "focus": "Show readiness for target role",
                "actions": ["Present outcomes to manager"],
            },
        ],
    }
    return plan