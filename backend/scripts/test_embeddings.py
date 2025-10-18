import json
import numpy as np
from backend.shared.embeddings import cosine

# Load generated data
with open("backend/data/profile_cache.json") as f:
    profiles_cache = json.load(f)

with open("backend/data/index_roles.json") as f:
    roles = json.load(f)

with open("backend/data/index_courses.json") as f:
    courses = json.load(f)

with open("backend/data/index_mentors.json") as f:
    mentors = json.load(f)

# Pick one profile vector (first employee)
first_vec = np.array(list(profiles_cache.values())[0]["vector"])
print("Employee vector dims:", first_vec.shape)

# Pick a role vector and compute cosine similarity
role_vec = np.array(roles[0]["vector"])
sim = cosine(first_vec, role_vec)
print(f"Similarity to role '{roles[0]['role']}':", round(sim, 3))

# Check for reasonable ranges
assert 0.0 <= sim <= 1.0, "Cosine out of range!"
assert len(first_vec) == len(role_vec), "Vector dimension mismatch"

# Quick aggregate sanity
print("Roles:", len(roles), "Courses:", len(courses), "Mentors:", len(mentors))
print("✅ Sanity check passed")