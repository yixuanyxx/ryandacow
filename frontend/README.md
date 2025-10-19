# PSA Workforce AI - Frontend MVP

## Overview
Minimal MVP frontend for PSA Workforce AI with 3 core pages:
- **Login Page** - Simple authentication
- **Dashboard Page** - AI recommendations display  
- **Chatbot Page** - AI conversation interface

## Tech Stack
- Vue 3 with Composition API
- Vue Router for navigation
- Pinia for state management
- Axios for API calls
- Plain CSS (no UI framework)

## Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Access the application:**
   - Frontend: http://localhost:5173
   - Backend APIs: 
     - User Management: http://localhost:5001
     - Recommendations: http://localhost:5004

## Demo Accounts

Use these demo accounts to test the login:

| Email | Password | Role |
|-------|----------|------|
| samantha.lee@globalpsa.com | demo123 | Cloud Solutions Architect |
| aisyah.rahman@globalpsa.com | demo123 | Cybersecurity Analyst |
| rohan.mehta@globalpsa.com | demo123 | Finance Manager (FP&A) |
| grace.lee@globalpsa.com | demo123 | Senior HR Business Partner |
| felicia.goh@globalpsa.com | demo123 | Treasury Analyst |

## Features

### Login Page
- Email/password authentication
- Integration with backend auth service
- Demo account suggestions
- Error handling

### Dashboard Page  
- User profile display
- AI-powered recommendations (courses, mentors, career paths)
- Navigation to chat interface
- Logout functionality

### Chatbot Page
- Real-time AI conversation
- Message history
- Clear chat functionality
- Back navigation to dashboard

## API Integration

The frontend integrates with these backend services:

- **Authentication**: `/api/auth/login` → User Management Service (Port 5001)
- **User Profile**: `/api/users/{id}` → User Management Service (Port 5001)  
- **Recommendations**: `/api/recommendations/{id}` → Recommendations Service (Port 5004)
- **AI Chat**: `/api/chat/message` → AI Chat Service (Port 5002)

## Project Structure

```
src/
├── views/
│   ├── LoginPage.vue           # Login interface
│   ├── DashboardPage.vue       # Main dashboard
│   └── ChatbotPage.vue         # AI chat interface
├── components/
│   └── common/
│       ├── BaseButton.vue      # Reusable button
│       ├── BaseInput.vue       # Reusable input
│       └── BaseCard.vue        # Reusable card
├── store/
│   ├── auth.js                 # Authentication state
│   └── chat.js                 # Chat state
├── services/
│   ├── api.js                  # Axios configuration
│   ├── authService.js          # Auth API calls
│   └── chatService.js          # Chat API calls
├── router/
│   └── index.js                # Route configuration
└── styles/
    └── main.css                # Global styles
```

## Development Notes

- Uses Vite for fast development
- Proxy configuration for API calls
- Local storage for auth persistence
- Responsive design with mobile support
- Error handling and loading states
- Clean, minimal UI design
