# Recommendations Service - Supabase Integration

## Overview
The recommendations service has been updated to fetch real data from Supabase instead of using hardcoded demo data.

## Database Tables
The service connects to two Supabase tables:
- `public.courses` - Contains course information
- `public.career_pathways` - Contains career pathway information

## Environment Variables
To enable Supabase integration, set these environment variables:

```bash
SUPABASE_URL=your_supabase_url_here
SUPABASE_SERVICE_KEY=your_supabase_service_key_here
DEMO_MODE=false
```

## API Endpoints

### Get All Recommendations
```
GET /recommendations/{user_id}
```
Returns course, mentor, and career pathway recommendations for the dashboard.

### Get Course Recommendations
```
GET /recommendations/courses/{user_id}
```
Returns personalized course recommendations.

### Get Career Pathway Recommendations
```
GET /recommendations/career-pathways/{user_id}
```
Returns career pathway recommendations.

### Get Mentor Recommendations
```
GET /recommendations/mentors/{user_id}
```
Returns mentor recommendations (currently demo data).

## Data Structure

### Courses Table Schema
```json
{
  "id": 1,
  "title": "AWS Cloud Architecture Certification",
  "description": "Comprehensive course on AWS cloud architecture patterns and best practices",
  "duration_weeks": 12,
  "required_skills": ["Cloud Architecture", "Infrastructure Design, Analysis & Architecture"],
  "created_at": "2025-10-18 04:16:20.694696+00"
}
```

### Career Pathways Table Schema
```json
{
  "id": 1,
  "name": "Cloud Solutions Architect Path",
  "description": "Progression path to senior cloud architecture roles",
  "target_role": "Senior Cloud Solutions Architect",
  "required_skills": ["Cloud Architecture", "Enterprise Architecture", "Cloud DevOps & Automation"],
  "created_at": "2025-10-18 04:16:20.694696+00"
}
```

## Fallback Behavior
If Supabase is not configured or unavailable, the service automatically falls back to demo data to ensure the application continues to work.

## Future Enhancements
- Implement real matching logic based on user skills and preferences
- Add mentor data to Supabase
- Implement caching for better performance
- Add user preference tracking
