# PSA Workforce AI - MVP Backend

## Overview

Minimal backend for hackathon demo focusing on AI-powered career guidance.

## Architecture

**3 Core Microservices:**

- **Auth Service** (Port 5001) - User authentication
- **AI Chat Service** (Port 5002) - Conversational AI
- **Recommendations Service** (Port 5003) - AI recommendations

## Database

**Simplified Schema:** `database/mvp_schema.sql`

- Users (demo accounts)
- Skills & User Skills
- Courses & Career Pathways
- AI Chat Sessions & Messages

## Demo Accounts

```json
{ "email": "sarah@psa.com", "password": "demo123" }
{ "email": "john@psa.com", "password": "demo123" }
{ "email": "mike@psa.com", "password": "demo123" }
```

## Quick Start

### 1. Database Setup

```bash
# Create Supabase project
# Run database/mvp_schema.sql in Supabase SQL editor
```

### 2. Environment Setup

Create `.env` in each microservice:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_supabase_key
JWT_SECRET=your_jwt_secret
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 3. Install Dependencies

```bash
cd user-management && pip install -r requirements.txt
cd ../ai_chat && pip install -r requirements.txt
cd ../recommendations && pip install -r requirements.txt
```

### 4. Run Services

```bash
# Terminal 1
cd user-management && python app.py

# Terminal 2
cd ai_chat && python app.py

# Terminal 3
cd recommendations && python app.py
```

## API Endpoints

### Auth Service (5001)

- `POST /auth/login` - Login with demo accounts
- `GET /auth/profile` - Get user profile

### AI Chat Service (5002)

- `POST /chat/message` - Send message to AI
- `GET /chat/history` - Get chat history
- `POST /chat/clear` - Clear chat history

### Recommendations Service (5003)

- `GET /recommendations/{user_id}` - Get dashboard recommendations
- `GET /recommendations/courses/{user_id}` - Get course recommendations
- `GET /recommendations/mentors/{user_id}` - Get mentor recommendations

## Features

### ✅ MVP Features

- **Simple Authentication** - Demo accounts only
- **AI Chatbot** - Predefined responses based on user context
- **Smart Recommendations** - Course, mentor, career suggestions
- **User Context** - Skills and profile-based personalization

### ❌ Not Included (for MVP)

- User registration
- Profile editing
- Real OpenAI integration
- Complex analytics
- Advanced matching algorithms
- File uploads
- Notifications

## Frontend Integration

The backend is designed to work with the minimal Vue.js frontend:

- **Login Page** → Auth Service
- **Dashboard** → Recommendations Service
- **Chat Page** → AI Chat Service

## Demo Flow

1. **Login** → `POST /auth/login` with demo credentials
2. **Dashboard** → `GET /recommendations/{user_id}` for AI suggestions
3. **Chat** → `POST /chat/message` for AI career advice
4. **Personalized Responses** → AI considers user skills and goals

## Development Notes

- **Mock AI Responses** - Predefined responses for demo
- **Simple Matching** - Basic algorithms for recommendations
- **Demo Data** - Pre-loaded users, skills, courses
- **No Real OpenAI** - Uses rule-based responses for hackathon

Perfect for hackathon demo! 🚀

## 🔍 AI Orchestration & Career Guidance (New Additions)

### Overview
Adds a complete **AI pipeline** for personalized career guidance that works both **offline (mock mode)** and **online (OpenAI-enabled)**.  
Implements embeddings, semantic catalogs, a recommender engine, leadership readiness scoring, and an orchestration layer exposed through `/chat/guidance`.

### Key Components
| File / Folder | Purpose |
|----------------|----------|
| `backend/shared/embeddings.py` | Handles text embeddings (uses mock vectors when no OpenAI key). |
| `backend/shared/recommender.py` | Core matching logic for roles, courses, mentors. |
| `backend/shared/leadership.py` | Leadership readiness scoring (offline). |
| `backend/ai_chat/orchestrator.py` | Chains recommender + leadership → structured career plan. |
| `backend/ai_chat/llm_client.py` | Summarizes plan using LLM or mock text if no key. |
| `backend/ai_chat/services/chat_service.py` | Integrates orchestration into the chat flow. |
| `backend/recommendations/bootstrap_indices.py` | Loads prebuilt JSON indices from `backend/data/`. |
| `backend/scripts/*` | Utility scripts for building or testing the AI pipeline. |

### Data Folder (required)
Create `backend/data/` with four JSONs (mock data included for offline demo):
profile_cache.json      # employee profiles
index_roles.json        # role catalog
index_courses.json      # course catalog
index_mentors.json      # mentor catalog

When OpenAI access is approved, rebuild real embeddings:
```bash
python -m backend.scripts.build_semantic_catalog