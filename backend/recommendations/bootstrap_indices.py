# backend/recommendations/bootstrap_indices.py
import json
import os
from typing import List, Dict

DATA_DIR = os.getenv("BACKEND_DATA_DIR", "backend/data")

def _load_json(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_roles(path: str | None = None) -> List[Dict]:
    p = path or os.path.join(DATA_DIR, "index_roles.json")
    if not os.path.exists(p):
        # Graceful empty fallback so your scripts can still run
        return []
    return _load_json(p)

def load_courses(path: str | None = None) -> List[Dict]:
    p = path or os.path.join(DATA_DIR, "index_courses.json")
    if not os.path.exists(p):
        return []
    return _load_json(p)

def load_mentors(path: str | None = None) -> List[Dict]:
    p = path or os.path.join(DATA_DIR, "index_mentors.json")
    if not os.path.exists(p):
        return []
    return _load_json(p)