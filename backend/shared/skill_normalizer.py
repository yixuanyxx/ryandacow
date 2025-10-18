import re

STOPWORDS = {"and", "&", "/", "-", "of", "for", "in", "to"} 

def normalize_skill(s: str) -> str:
    if not s: return ""
    s = s.lower().strip()
    s = s.replace("&", "and")
    s = re.sub(r"[\s/]+", " ", s)
    s = s.replace("-", " ")
    s = " ".join(w for w in s.split() if w not in STOPWORDS)
    return s

def normalize_list(skills):
    return [normalize_skill(x) for x in (skills or []) if normalize_skill(x)]