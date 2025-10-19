# backend/shared/llm_clients.py
import os
from openai import OpenAI

def get_apim_client_for(deployment: str) -> OpenAI:
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "").rstrip("/")
    version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")
    key = os.getenv("AZURE_OPENAI_API_KEY_PRIMARY") or os.getenv("AZURE_OPENAI_API_KEY_SECONDARY")
    if not (endpoint and key):
        raise RuntimeError("Missing APIM endpoint or key")

    # Correct for PSA gateway
    base_url = f"{endpoint}/{deployment}/openai/deployments/{deployment}"
    return OpenAI(
        base_url=base_url,
        api_key=key,
        default_headers={"api-key": key},
        default_query={"api-version": version},
    )