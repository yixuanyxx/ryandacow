# backend/shared/recommender.py

import numpy as np
from typing import Dict, List
from embeddings import embed_text, cosine
from skill_normalizer import normalize_list

# --- Helper to convert lists to numpy arrays ---
def _as_np(v): 
    return np.array(v, dtype=float)


# =====================================================
# 1️⃣ ROLE RECOMMENDATION
# =====================================================
def role_recommendations(employee: Dict, role_index: List[Dict], top_k: int = 5) -> List[Dict]:
    """
    Compute the top K roles that best fit the employee.
    Combines embedding similarity + skill gap ratio + title alignment.
    """
    e_vec = _as_np(employee["vector"])
    e_skills = set(normalize_list(employee.get("skills", [])))

    scored = []
    for r in role_index:
        r_vec = _as_np(r["vector"])
        sim = cosine(e_vec, r_vec)

        req_skills = set(normalize_list(r.get("required_skills", [])))
        missing = [s for s in req_skills if s not in e_skills]
        gap_ratio = len(missing) / max(1, len(req_skills))

        # Bonus: measure how similar the employee’s job title is to the target role
        title_sim = cosine(embed_text(employee["job_title"]), embed_text(r["role"]))

        score = 0.6 * sim + 0.3 * (1 - gap_ratio) + 0.1 * title_sim
        scored.append({
            "role_id": r["id"],
            "role": r["role"],
            "score": round(100 * score, 1),
            "missing_skills": missing,
        })

    # Sort descending by composite score
    return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]


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