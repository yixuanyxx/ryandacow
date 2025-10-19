## 🔍 AI Orchestration & Career Guidance (New Additions)

### Overview

Adds a complete **AI pipeline** for personalized career guidance that works both **offline (mock mode)** and **online (OpenAI-enabled)**.\
Implements embeddings, semantic catalogs, a recommender engine, leadership readiness scoring, and an orchestration layer exposed through `/chat/guidance`.

### Key Components

| File / Folder                                  | Purpose                                                         |
| ---------------------------------------------- | --------------------------------------------------------------- |
| `backend/shared/embeddings.py`                 | Handles text embeddings (uses mock vectors when no OpenAI key). |
| `backend/shared/recommender.py`                | Core matching logic for roles, courses, mentors.                |
| `backend/shared/leadership.py`                 | Leadership readiness scoring (offline).                         |
| `backend/ai_chat/orchestrator.py`              | Chains recommender + leadership → structured career plan.       |
| `backend/ai_chat/llm_client.py`                | Summarizes plan using LLM or mock text if no key.               |
| `backend/ai_chat/services/chat_service.py`     | Integrates orchestration into the chat flow.                    |
| `backend/recommendations/bootstrap_indices.py` | Loads prebuilt JSON indices from `backend/data/`.               |
| `backend/scripts/*`                            | Utility scripts for building or testing the AI pipeline.        |

### Data Folder (required)

Create `backend/data/` with four JSONs (mock data included for offline demo):

```
profile_cache.json      # employee profiles
index_roles.json        # role catalog
index_courses.json      # course catalog
index_mentors.json      # mentor catalog
```

When OpenAI access is approved, rebuild real embeddings:

```bash
python -m backend.scripts.build_semantic_catalog
```

### New Endpoint

**Service:** AI Chat (port 5002)

| Method | Endpoint         | Description                                  |
| ------ | ---------------- | -------------------------------------------- |
| `POST` | `/chat/guidance` | Generates a full career-plan JSON + summary. |

**Body**

```json
{ "message": "I want to be a tech lead", "user_id": 1 }
```

**Response**

```json
{
  "Code": 200,
  "Message": "AI guidance generated",
  "data": {
    "summary": "...",
    "plan": { "target_role": "Tech Lead", "fit_score": 82.1, ... },
    "leadership": { "score": 63.5, "level": "Developing", ... },
    "alternatives": [...]
  }
}
```

If indices aren’t built yet, the service returns:

```json
{ "Code": 503, "Message": "Guidance unavailable (indices not built yet)." }
```

### Environment Variables

Add to your root `.env`:

```
OPENAI_API_KEY=           # optional; leave blank for mock mode
OPENAI_MODEL=gpt-4o-mini
SUPABASE_URL=...
SUPABASE_SERVICE_KEY=...
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
EMBED_MODEL=text-embedding-3-small
```

### Testing the AI Flow

```bash
python -m backend.scripts.run_orchestrator_once     # prints full mock plan JSON
curl -X POST http://localhost:5002/chat/guidance \
     -H "Content-Type: application/json" \
     -d '{"message":"career plan","user_id":1}'
```

### Notes for Teammates

- Works **offline** with mock JSONs → instant integration with frontend.
- Auto-upgrades to **real OpenAI embeddings** when a valid key is present.
- Returns structured JSON so frontend can render role cards, course lists, mentor suggestions, and leadership metrics.

