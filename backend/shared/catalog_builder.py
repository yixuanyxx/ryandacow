from typing import List, Dict, Optional
import json, os
import pandas as pd
from backend.shared.embeddings import embed_text
from backend.shared.skill_normalizer import normalize_list, normalize_skill

def _embed_field_join(parts: List[str]) -> list[float]:
    text = " | ".join([p for p in parts if p])
    return embed_text(text).tolist()

def build_roles_from_excel(xlsx_path: str, sheet: Optional[str] = None) -> List[Dict]:
    """
    Expect columns similar to:
    - 'Role' or 'Function' or 'Job Title'
    - 'Description' (optional)
    - 'Required Skills' (comma/semicolon separated) OR separate columns for skills
    We keep it defensive so slight column name variations don't break us.
    """
    df = pd.read_excel(xlsx_path, sheet_name=sheet) if sheet else pd.read_excel(xlsx_path)
    cols = {c.lower(): c for c in df.columns}

    # heuristics for column names
    role_col = cols.get("role") or cols.get("function") or cols.get("job title") or list(df.columns)[0]
    desc_col = cols.get("description") or None
    req_col  = cols.get("required skills") or cols.get("skills") or None

    roles = []
    for i, row in df.iterrows():
        role = str(row.get(role_col, "")).strip()
        if not role:
            continue
        desc = str(row.get(desc_col, "")).strip() if desc_col else ""
        if req_col:
            raw = row.get(req_col, "")
            if pd.isna(raw): raw = ""
            req_sk = [s.strip() for s in str(raw).replace(";", ",").split(",") if s.strip()]
        else:
            # try to gather skills from any column that contains 'skill'
            req_sk = []
            for c in df.columns:
                if "skill" in c.lower():
                    val = row.get(c, "")
                    if pd.isna(val): continue
                    req_sk.extend([s.strip() for s in str(val).replace(";", ",").split(",") if s.strip()])

        req_sk = normalize_list(req_sk)
        vec = _embed_field_join([role, desc, "required: " + ", ".join(req_sk)])
        roles.append({
            "id": i + 1,  # simple stable id by row index; replace with real id if you have one
            "role": role,
            "description": desc,
            "required_skills": req_sk,
            "vector": vec
        })
    return roles

def build_courses_seed(courses: List[Dict]) -> List[Dict]:
    """
    courses: [{id,title,description,required_skills:[...]}]
    """
    out = []
    for c in courses:
        req = normalize_list(c.get("required_skills", []))
        vec = _embed_field_join([c.get("title",""), c.get("description",""), "skills: " + ", ".join(req)])
        out.append({**c, "required_skills": req, "vector": vec})
    return out

def build_mentors_from_profiles(profiles: List[Dict]) -> List[Dict]:
    """
    profiles: output from your ProfileIngestor/loader (already normalized/embedded employees).
    We'll *re-embed* mentors with a text more focused on mentorship.
    """
    out = []
    for p in profiles:
        skills = normalize_list(p.get("skills", []))
        blob_parts = [
            p.get("name",""),
            p.get("job_title",""),
            "skills: " + ", ".join(skills),
            # if you later add 'bio' or 'achievements', include them here
        ]
        vec = _embed_field_join(blob_parts)
        out.append({
            "id": p["employee_id"],
            "name": p["name"],
            "job_title": p["job_title"],
            "skills": skills,
            "bio": "",  # fill later if you have one
            "vector": vec
        })
    return out

def save_index(data: List[Dict], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)