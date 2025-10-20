# backend/recommendations/bootstrap_indices.py
from dotenv import load_dotenv; load_dotenv()
import os, json
from pathlib import Path
from typing import List, Dict

def _data_dir() -> Path:
    env = os.getenv("BACKEND_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    # default to backend/data next to repo
    # Try multiple possible locations
    possible_paths = [
        Path(__file__).parent / ".." / ".." / "data",  # from recommendations
        Path(__file__).parent / ".." / "data",         # from backend
        Path(__file__).parent / "data",                # same directory
        Path.cwd() / "data",                           # current working directory
        Path.cwd() / "backend" / "data"                # backend/data from project root
    ]
    
    for path in possible_paths:
        resolved_path = path.resolve()
        if resolved_path.exists():
            return resolved_path
    
    # If none found, return the first option and let it fail with a clear error
    return (Path(__file__).parent / ".." / ".." / "data").resolve()

def _load_json(name: str) -> List[Dict]:
    p = _data_dir() / name
    if not p.exists():
        raise FileNotFoundError(f"Index file not found: {p}")
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def load_roles() -> List[Dict]:
    return _load_json("index_roles.json")

def load_courses() -> List[Dict]:
    return _load_json("index_courses.json")

def load_mentors() -> List[Dict]:
    return _load_json("index_mentors.json")