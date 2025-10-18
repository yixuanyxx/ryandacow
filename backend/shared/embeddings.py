import os, hashlib
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
_CACHE = {}

def embed_text(text: str) -> np.ndarray:
    key = hashlib.sha1((text or "").lower().encode()).hexdigest()
    if key in _CACHE:
        return np.array(_CACHE[key])
    v = client.embeddings.create(model=MODEL, input=text).data[0].embedding
    _CACHE[key] = v
    return np.array(v)

def cosine(a, b) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))