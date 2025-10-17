# PSA Workforce Compass - Microservices Backend Setup

## Overview
This backend is organized into microservices, each handling a specific domain of the PSA Workforce Compass system.

## Microservices Architecture

### 1. **User Management** (Port 5001)
- **Domain**: User authentication, profiles, personal information
- **Tables**: users, user_personal_info, user_languages, employment_info, position_history, education
- **Key Features**: Registration, login, profile management

### 2. **Skills Management** (Port 5002)
- **Domain**: Skills taxonomy, competencies, experience tracking
- **Tables**: function_areas, specializations, skills, user_skills, competencies, user_competencies, experience_types, user_experiences, projects
- **Key Features**: Skills matrix, competency tracking, experience management

### 3. **Career Development** (Port 5003)
- **Domain**: Career pathways, goal setting, recommendations
- **Tables**: career_pathways, pathway_requirements, user_career_goals
- **Key Features**: Career recommendations, goal tracking, skill gap analysis

### 4. **AI Recommendation** (Port 5004)
- **Domain**: AI-powered advice and chatbot
- **Tables**: ai_chat_sessions, ai_chat_messages
- **Key Features**: OpenAI integration, personalized advice, quick suggestions

### 5. **Mentorship** (Port 5005)
- **Domain**: Mentor-mentee matching and management
- **Tables**: mentorship_requests
- **Key Features**: Smart matching, request management

### 6. **Training** (Port 5006)
- **Domain**: Course management and progress tracking
- **Tables**: courses, user_training
- **Key Features**: Course catalog, enrollment, progress tracking

### 7. **Analytics** (Port 5007)
- **Domain**: Analytics, metrics, dashboard data
- **Tables**: user_analytics, notifications
- **Key Features**: Leadership scoring, engagement metrics, insights

## Database Schema

The comprehensive Supabase schema is located in `database/supabase_schema.sql` and includes:

### Core Tables
- **users** - User authentication and basic info
- **user_personal_info** - Extended personal information
- **user_languages** - Language proficiencies
- **employment_info** - Job and department information
- **position_history** - Career progression history
- **education** - Educational background

### Skills & Competencies
- **function_areas** - Top-level skill categories (Info Tech: Infrastructure, Finance, etc.)
- **specializations** - Mid-level categories (Cloud Computing: Cloud Architecture, etc.)
- **skills** - Individual skills (Cloud Architecture, Python, etc.)
- **user_skills** - User skill proficiencies with levels
- **competencies** - Soft skills and competencies
- **user_competencies** - User competency levels

### Experience & Projects
- **experience_types** - Types of experience (Program, Rotation, Exercise, etc.)
- **user_experiences** - User's professional experiences
- **projects** - Project participation and outcomes

### Career Development
- **career_pathways** - Defined career progression paths
- **pathway_requirements** - Skills required for each pathway
- **user_career_goals** - User's career objectives

### Training & Learning
- **courses** - Available training courses
- **user_training** - User enrollment and progress

### Mentorship
- **mentorship_requests** - Mentor-mentee relationships

### AI & Analytics
- **ai_chat_sessions** - AI conversation sessions
- **ai_chat_messages** - Individual chat messages
- **user_analytics** - User metrics and analytics
- **notifications** - System notifications

## Setup Instructions

### 1. Database Setup
```bash
# Create Supabase project at https://supabase.com
# Run the schema file in Supabase SQL editor
cat database/supabase_schema.sql
```

### 2. Environment Configuration
Create `.env` file in each microservice:
```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# OpenAI Configuration (for AI microservice)
OPENAI_API_KEY=your_openai_api_key

# JWT Configuration
JWT_SECRET=your_jwt_secret_key_change_in_production

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Install Dependencies
```bash
# Install shared dependencies
pip install flask flask-cors python-dotenv supabase pyjwt openai requests

# Or create requirements.txt in each microservice
```

### 4. Run Microservices
```bash
# Terminal 1 - User Management
cd user-management && python app.py

# Terminal 2 - Skills Management
cd skills-management && python app.py

# Terminal 3 - Career Development
cd career-development && python app.py

# Terminal 4 - AI Recommendation
cd ai-recommendation && python app.py

# Terminal 5 - Mentorship
cd mentorship && python app.py

# Terminal 6 - Training
cd training && python app.py

# Terminal 7 - Analytics
cd analytics && python app.py
```

## API Gateway (Optional)

For production, consider using an API gateway like Kong or Nginx to route requests to the appropriate microservice.

## Data Flow

1. **User Registration/Login** → User Management (5001)
2. **Profile Updates** → User Management (5001)
3. **Skills Management** → Skills Management (5002)
4. **Career Planning** → Career Development (5003)
5. **AI Chat** → AI Recommendation (5004)
6. **Mentorship** → Mentorship (5005)
7. **Training** → Training (5006)
8. **Analytics** → Analytics (5007)

## Sample Data

The schema includes sample data for:
- Function areas and specializations
- Skills taxonomy
- Competencies
- Experience types
- Career pathways
- Sample courses

## Development Notes

- Each microservice is independent and can be developed/deployed separately
- Shared components are in the `shared/` directory
- Database connections use Supabase client
- Authentication uses JWT tokens
- CORS is configured for frontend integration

## Production Considerations

- Use environment-specific configurations
- Implement proper logging and monitoring
- Add rate limiting and security measures
- Consider database connection pooling
- Implement health checks for each microservice
- Use containerization (Docker) for deployment
