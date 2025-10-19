# backend/shared/embeddings.py
from dotenv import load_dotenv; load_dotenv()

import os, time
from typing import List, Union
from backend.shared.llm_clients import get_apim_client_for

# Deployment name (from .env)
DEPLOY_EMBED = os.getenv("AZURE_DEPLOY_EMBED", "text-embedding-3-small")

# --- client singleton for this deployment ---
_client = None
def _client_once():
    global _client
    if _client is None:
        _client = get_apim_client_for(DEPLOY_EMBED)
    return _client

# --- Core single-call embedding ---
def _embed_batch(texts: List[str]) -> List[List[float]]:
    resp = _client_once().embeddings.create(
        model=DEPLOY_EMBED,  # APIM expects the deployment name here
        input=texts
    )
    return [d.embedding for d in resp.data]

def embed_many(texts: List[str], batch_size: int = 64, max_retries: int = 3) -> List[List[float]]:
    out: List[List[float]] = []
    for i in range(0, len(texts), batch_size):
        chunk = texts[i:i+batch_size]
        for attempt in range(max_retries):
            try:
                out.extend(_embed_batch(chunk))
                break
            except Exception:
                if attempt == max_retries - 1:
                    raise
                time.sleep(1.5 * (attempt + 1))  # basic backoff
    return out

def embed_text(text: str) -> List[float]:
    return embed_many([text])[0]

# cosine helper (unchanged)
def cosine(a: Union[List[float], "np.ndarray"], b: Union[List[float], "np.ndarray"]) -> float:
    import numpy as np
    a = np.array(a, dtype=float); b = np.array(b, dtype=float)
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0: return 0.0
    return float(np.dot(a, b) / denom)