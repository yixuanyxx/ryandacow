# PSA Workforce AI MVP - API Documentation

## Overview

This document provides comprehensive API documentation for the PSA Workforce AI MVP backend services. The system consists of two main microservices:

- **User Management Service** (Port 5001): Handles authentication and user profile management
- **Recommendations Service** (Port 5004): Provides AI-powered career recommendations

## Base URLs

- User Management: `http://localhost:5001`
- Recommendations: `http://localhost:5004`

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

## User Management Service (Port 5001)

### Authentication Endpoints

#### POST /auth/login
Login user with demo credentials.

**Request:**
```json
{
  "email": "samantha.lee@globalpsa.com",
  "password": "demo123"
}
```

**Response:**
```json
{
  "Message": "Login successful",
  "data": {
    "user": {
      "id": "EMP-20001",
      "email": "samantha.lee@globalpsa.com",
      "name": "Samantha Lee",
      "job_title": "Cloud Solutions Architect",
      "department": "Information Technology",
      "unit": "Infrastructure Architecture & Cloud",
      "line_manager": "Victor Tan"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### GET /auth/profile
Get authenticated user's profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "Message": "Success",
  "data": {
    "user": {
      "id": "EMP-20001",
      "email": "samantha.lee@globalpsa.com",
      "name": "Samantha Lee",
      "job_title": "Cloud Solutions Architect",
      "department": "Information Technology",
      "unit": "Infrastructure Architecture & Cloud",
      "line_manager": "Victor Tan",
      "in_role_since": "2022-07-01",
      "hire_date": "2016-03-15",
      "last_updated": "2025-10-09"
    },
    "skills": [
      {
        "id": 1,
        "user_id": "EMP-20001",
        "skill_id": 64,
        "skills": {
          "id": 64,
          "function / unit / skill": "Info Tech: Infrastructure",
          "specialisation / unit": "Cloud Computing: Cloud Architecture"
        }
      }
    ]
  }
}
```

### User Management Endpoints

#### GET /users/{user_id}
Get user profile by employee ID.

**Parameters:**
- `user_id` (string): Employee ID (e.g., "EMP-20001")

**Response:**
```json
{
  "Message": "Success",
  "data": {
    "user": {
      "id": "EMP-20001",
      "email": "samantha.lee@globalpsa.com",
      "name": "Samantha Lee",
      "job_title": "Cloud Solutions Architect",
      "department": "Information Technology",
      "unit": "Infrastructure Architecture & Cloud",
      "line_manager": "Victor Tan",
      "in_role_since": "2022-07-01",
      "hire_date": "2016-03-15",
      "last_updated": "2025-10-09"
    },
    "skills": [
      {
        "id": 1,
        "user_id": "EMP-20001",
        "skill_id": 64,
        "skills": {
          "id": 64,
          "function / unit / skill": "Info Tech: Infrastructure",
          "specialisation / unit": "Cloud Computing: Cloud Architecture"
        }
      }
    ]
  }
}
```

#### GET /users/department/{department}
Get all users in a specific department.

**Parameters:**
- `department` (string): Department name (e.g., "Information Technology")

**Response:**
```json
{
  "Message": "Success",
  "data": [
    {
      "id": "EMP-20001",
      "email": "samantha.lee@globalpsa.com",
      "name": "Samantha Lee",
      "job_title": "Cloud Solutions Architect",
      "department": "Information Technology",
      "unit": "Infrastructure Architecture & Cloud",
      "line_manager": "Victor Tan",
      "in_role_since": "2022-07-01",
      "hire_date": "2016-03-15",
      "last_updated": "2025-10-09"
    },
    {
      "id": "EMP-20002",
      "email": "aisyah.rahman@globalpsa.com",
      "name": "Nur Aisyah Binte Rahman",
      "job_title": "Cybersecurity Analyst",
      "department": "Information Technology",
      "unit": "Cybersecurity Operations",
      "line_manager": "Daniel Chua",
      "in_role_since": "2024-07-01",
      "hire_date": "2023-01-15",
      "last_updated": "2025-10-09"
    }
  ]
}
```

## Recommendations Service (Port 5004)

### Recommendation Endpoints

#### GET /recommendations/{user_id}
Get comprehensive recommendations for user dashboard.

**Parameters:**
- `user_id` (string): Employee ID (e.g., "EMP-20001")

**Response:**
```json
{
  "Message": "Success",
  "data": {
    "recommendations": [
      {
        "type": "course",
        "title": "AWS Cloud Architecture Certification",
        "description": "Comprehensive course on AWS cloud architecture patterns and best practices",
        "match_score": 92,
        "metadata": {
          "duration_weeks": 12,
          "required_skills": ["Cloud Architecture", "Infrastructure Design, Analysis & Architecture"]
        }
      },
      {
        "type": "mentor",
        "title": "John Smith",
        "description": "Senior Cloud Architect with extensive experience",
        "match_score": 88,
        "metadata": {
          "job_title": "Senior Cloud Architect",
          "department": "Information Technology",
          "experience_years": 15
        }
      },
      {
        "type": "career",
        "title": "Cloud Solutions Architect Path",
        "description": "Next step: Cloud Solutions Architect Path - Progression path to senior cloud architecture roles",
        "match_score": 85,
        "metadata": {
          "target_role": "Senior Cloud Solutions Architect",
          "required_skills": ["Cloud Architecture", "Enterprise Architecture", "Cloud DevOps & Automation"]
        }
      }
    ],
    "user_name": "Samantha Lee",
    "job_title": "Cloud Solutions Architect",
    "department": "Information Technology"
  }
}
```

#### GET /recommendations/courses/{user_id}
Get personalized course recommendations.

**Parameters:**
- `user_id` (string): Employee ID (e.g., "EMP-20001")

**Response:**
```json
{
  "Message": "Success",
  "data": [
    {
      "id": 1,
      "title": "AWS Cloud Architecture Certification",
      "description": "Comprehensive course on AWS cloud architecture patterns and best practices",
      "duration_weeks": 12,
      "match_score": 95.0,
      "required_skills": ["Cloud Architecture", "Infrastructure Design, Analysis & Architecture"]
    },
    {
      "id": 2,
      "title": "Advanced Cloud Security",
      "description": "Advanced security practices for cloud environments",
      "duration_weeks": 8,
      "match_score": 87.0,
      "required_skills": ["Securing Cloud Infrastructure", "Network Security Management"]
    },
    {
      "id": 3,
      "title": "Enterprise Architecture Patterns",
      "description": "Design patterns for enterprise-scale cloud architectures",
      "duration_weeks": 10,
      "match_score": 82.0,
      "required_skills": ["Enterprise Architecture", "Infrastructure Design, Analysis & Architecture"]
    }
  ]
}
```

#### GET /recommendations/mentors/{user_id}
Get mentor recommendations.

**Parameters:**
- `user_id` (string): Employee ID (e.g., "EMP-20001")

**Response:**
```json
{
  "Message": "Success",
  "data": [
    {
      "id": "EMP-20002",
      "name": "Nur Aisyah Binte Rahman",
      "job_title": "Cybersecurity Analyst",
      "department": "Information Technology",
      "match_score": 88.0,
      "skills": ["Vulnerability Management", "Network Security Management", "Cybersecurity Threat Intelligence and Detection"]
    },
    {
      "id": "EMP-20003",
      "name": "Rohan Mehta",
      "job_title": "Finance Manager (FP&A)",
      "department": "Finance",
      "match_score": 75.0,
      "skills": ["Financial Planning and Analysis", "Cost Management and Budget", "Financial Modeling"]
    },
    {
      "id": "EMP-20004",
      "name": "Grace Lee",
      "job_title": "Senior HR Business Partner",
      "department": "Human Resource",
      "match_score": 70.0,
      "skills": ["Generalist / Business Partner", "Talent Management", "Staff Development and Engagement"]
    }
  ]
}
```

## Error Responses

All endpoints return consistent error responses:

```json
{
  "Message": "Bad Request - Invalid input parameters"
}
```

```json
{
  "Message": "Unauthorized - Invalid credentials or missing token"
}
```

```json
{
  "Message": "Not Found - Resource not found"
}
```

```json
{
  "Message": "Internal Server Error - Server error occurred"
}
```

## Demo User Accounts

For testing purposes, use these demo accounts:

| Email | Password | Employee ID | Name | Job Title |
|-------|----------|-------------|------|-----------|
| samantha.lee@globalpsa.com | demo123 | EMP-20001 | Samantha Lee | Cloud Solutions Architect |
| aisyah.rahman@globalpsa.com | demo123 | EMP-20002 | Nur Aisyah Binte Rahman | Cybersecurity Analyst |
| rohan.mehta@globalpsa.com | demo123 | EMP-20003 | Rohan Mehta | Finance Manager (FP&A) |
| grace.lee@globalpsa.com | demo123 | EMP-20004 | Grace Lee | Senior HR Business Partner |
| felicia.goh@globalpsa.com | demo123 | EMP-20005 | Felicia Goh | Treasury Analyst |

## Frontend Integration Notes

### 1. Authentication Flow
1. User enters email and password
2. POST to `/auth/login` with credentials
3. Store JWT token from response
4. Include token in Authorization header for protected endpoints

### 2. Dashboard Data
1. GET `/auth/profile` to get user profile and skills
2. GET `/recommendations/{user_id}` to get comprehensive recommendations
3. Display user info, skills, and recommendations on dashboard

### 3. Course Recommendations
1. GET `/recommendations/courses/{user_id}` to get course recommendations
2. Display courses with match scores and required skills

### 4. Mentor Matching
1. GET `/recommendations/mentors/{user_id}` to get mentor recommendations
2. Display mentors with match scores and skills

### 5. User Search
1. GET `/users/department/{department}` to get users by department
2. GET `/users/{user_id}` to get specific user profile

## CORS Configuration

All services are configured with CORS to allow frontend requests:
- Origins: `*` (all origins allowed)
- Methods: GET, POST, PUT, DELETE
- Headers: Content-Type, Authorization

## Rate Limiting

Currently no rate limiting is implemented. Consider implementing rate limiting for production use.

## Testing

Use the provided test script to verify all endpoints:

```bash
cd backend
python3 test_endpoints.py
```

Or test manually with curl:

```bash
# Login
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"samantha.lee@globalpsa.com","password":"demo123"}'

# Get user profile
curl http://localhost:5001/users/EMP-20001

# Get recommendations
curl http://localhost:5004/recommendations/EMP-20001
```

## Database Schema

The API works with the following Supabase tables:

- `users`: User profiles with employee information
- `user_skills`: User skill associations
- `skills`: Skill definitions
- `courses`: Available courses
- `career_pathways`: Career progression paths
- `ai_chat_sessions`: Chat session tracking
- `ai_chat_messages`: Chat message history

## Version History

- v1.0.0: Initial MVP implementation with basic authentication and recommendations
