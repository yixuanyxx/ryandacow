import os
import json
from backend.shared.profile_ingestor import ProfileIngestor
from backend.shared.catalog_builder import (
    build_roles_from_excel, build_courses_seed, build_mentors_from_profiles, save_index
)

DATA_DIR = os.getenv("BACKEND_DATA_DIR", "backend/data")
SRC_JSON = os.getenv("EMPLOYEE_JSON", os.path.join(DATA_DIR, "Employee_Profiles.json"))
SRC_XLSX = os.getenv("FUNCTIONS_XLSX", os.path.join(DATA_DIR, "Functions & Skills.xlsx"))

# fallback to /mnt/data if local files don’t exist
if not os.path.exists(SRC_JSON) and os.path.exists("/mnt/data/Employee_Profiles.json"):
    SRC_JSON = "/mnt/data/Employee_Profiles.json"
if not os.path.exists(SRC_XLSX) and os.path.exists("/mnt/data/Functions & Skills.xlsx"):
    SRC_XLSX = "/mnt/data/Functions & Skills.xlsx"

# 1) employees -> for mentors index
profiles = ProfileIngestor(cache_path=os.path.join(DATA_DIR, "profile_cache.json")) \
    .ingest_profiles(SRC_JSON)

# 2) roles -> from Excel
roles = build_roles_from_excel(SRC_XLSX) 
save_index(roles, os.path.join(DATA_DIR, "index_roles.json"))

# 3) courses -> seed for now (replace with DB later)
seed_courses = [
    {"id": 101, "title": "Advanced Systems Design", "description": "Patterns, tradeoffs, non-functional requirements", "required_skills": ["systems design"]},
    {"id": 102, "title": "Stakeholder Management for Engineers", "description": "Influence without authority", "required_skills": ["stakeholder and partnership management"]},
    {"id": 103, "title": "Optimization in Port Operations", "description": "Routing, scheduling, constraints", "required_skills": ["optimization", "data analysis"]}
]
courses = build_courses_seed(seed_courses)
save_index(courses, os.path.join(DATA_DIR, "index_courses.json"))

# 4) mentors -> from profiles
mentors = build_mentors_from_profiles(profiles)
save_index(mentors, os.path.join(DATA_DIR, "index_mentors.json"))

print("Built catalog:")
print("  roles   :", len(roles))
print("  courses :", len(courses))
print("  mentors :", len(mentors))