import os, hashlib
import numpy as np
from dotenv import load_dotenv
load_dotenv()

# Only import OpenAI if API key is available
client = None
MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
_CACHE = {}

# Initialize client only if API key is available
if os.getenv("OPENAI_API_KEY"):
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    except ImportError:
        pass

def embed_text(text: str) -> np.ndarray:
    # If no OpenAI client, return mock embedding
    if not client:
        # Generate deterministic mock embedding based on text hash
        key = hashlib.sha1((text or "").lower().encode()).hexdigest()
        if key in _CACHE:
            return np.array(_CACHE[key])
        
        # Create mock embedding (150 dimensions for text-embedding-3-small)
        mock_embedding = np.random.RandomState(int(key[:8], 16)).normal(0, 0.1, 150)
        _CACHE[key] = mock_embedding
        return np.array(mock_embedding)
    
    # Use real OpenAI API
    key = hashlib.sha1((text or "").lower().encode()).hexdigest()
    if key in _CACHE:
        return np.array(_CACHE[key])
    v = client.embeddings.create(model=MODEL, input=text).data[0].embedding
    _CACHE[key] = v
    return np.array(v)

def cosine(a, b) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))