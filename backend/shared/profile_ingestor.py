import json, os, hashlib
from typing import Dict, List, Optional
from datetime import datetime
from backend.shared.embeddings import embed_text

class ProfileIngestor:
    """
    A reusable profile ingestion + embedding pipeline.
    Works with JSON from file or API.
    Automatically embeds new/updated profiles only.
    """

    def __init__(self, cache_path: Optional[str] = None):
        # Optional cache to store previous embeddings (avoid re-embedding)
        self.cache_path = cache_path or "profile_cache.json"
        self.cache = self._load_cache()

    def _load_cache(self) -> Dict:
        if os.path.exists(self.cache_path):
            with open(self.cache_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_path, "w", encoding="utf-8") as f:
            json.dump(self.cache, f, indent=2)

    def _hash_profile(self, p: Dict) -> str:
        # Hash profile to detect changes
        content = json.dumps(p, sort_keys=True)
        return hashlib.sha1(content.encode()).hexdigest()

    def _build_blob(self, e: Dict) -> str:
        job = e.get("employment_info", {}).get("job_title", "")
        dept = e.get("employment_info", {}).get("department", "")
        skills = [s.get("skill_name","") for s in e.get("skills", [])]
        comps = [c.get("name","") for c in e.get("competencies", [])]
        projects = [p.get("description","") for p in e.get("projects", [])]
        return " | ".join([
            job, dept,
            "skills: " + ", ".join(skills),
            "competencies: " + ", ".join(comps),
            "projects: " + " || ".join(projects)
        ])

    def ingest_profiles(self, source: str | List[Dict]) -> List[Dict]:
        """Load and embed profiles from JSON file or list of dicts."""
        # 1️⃣ Load data
        if isinstance(source, str):
            with open(source, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = source

        processed = []
        for e in data:
            employee_id = str(e.get("employee_id"))
            profile_hash = self._hash_profile(e)
            cached = self.cache.get(employee_id)

            # 2️⃣ If profile unchanged, reuse embedding
            if cached and cached.get("hash") == profile_hash:
                vec = cached["vector"]
            else:
                blob = self._build_blob(e)
                vec = embed_text(blob).tolist()
                self.cache[employee_id] = {
                    "hash": profile_hash,
                    "vector": vec,
                    "last_embedded": datetime.now().isoformat()
                }

            # 3️⃣ Normalized structure
            processed.append({
                "employee_id": employee_id,
                "name": e.get("personal_info", {}).get("name", ""),
                "job_title": e.get("employment_info", {}).get("job_title", ""),
                "department": e.get("employment_info", {}).get("department", ""),
                "skills": [s.get("skill_name","") for s in e.get("skills", [])],
                "competencies": [c.get("name","") for c in e.get("competencies", [])],
                "vector": vec,
            })

        self._save_cache()
        return processed