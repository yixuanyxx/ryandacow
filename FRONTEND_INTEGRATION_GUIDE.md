# PSA Workforce AI MVP - Frontend Integration Guide

## 🎯 Overview

This guide provides everything the frontend team needs to integrate with the PSA Workforce AI MVP backend services.

## 📁 Key Files

- **`API.md`** - Complete API documentation with all endpoints
- **`test_endpoints.py`** - Test script to verify endpoint functionality
- **`SETUP_GUIDE.md`** - Database setup and troubleshooting guide

## 🚀 Quick Start

### 1. Start Backend Services

```bash
# Terminal 1 - User Management Service (Port 5001)
cd backend/user-management
python3 app.py

# Terminal 2 - Recommendations Service (Port 5004)
cd backend/recommendations
python3 app.py
```

### 2. Test Services

```bash
cd backend
python3 test_endpoints.py
```

## 📊 API Endpoints Summary

### User Management Service (Port 5001)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/login` | Login user | No |
| GET | `/auth/profile` | Get user profile | Yes |
| GET | `/users/{user_id}` | Get user by ID | No |
| GET | `/users/department/{department}` | Get users by department | No |

### Recommendations Service (Port 5004)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/recommendations/{user_id}` | Get all recommendations | No |
| GET | `/recommendations/courses/{user_id}` | Get course recommendations | No |
| GET | `/recommendations/mentors/{user_id}` | Get mentor recommendations | No |

## 🔑 Authentication Flow

### 1. Login Request
```javascript
const loginResponse = await fetch('http://localhost:5001/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'samantha.lee@globalpsa.com',
    password: 'demo123'
  })
});

const loginData = await loginResponse.json();
const token = loginData.data.token;
```

### 2. Authenticated Requests
```javascript
const profileResponse = await fetch('http://localhost:5001/auth/profile', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  }
});
```

## 📱 Frontend Integration Examples

### Vue.js Integration

```javascript
// services/api.js
import axios from 'axios';

const API_BASE = {
  userManagement: 'http://localhost:5001',
  recommendations: 'http://localhost:5004'
};

// Auth service
export const authService = {
  async login(email, password) {
    const response = await axios.post(`${API_BASE.userManagement}/auth/login`, {
      email, password
    });
    return response.data;
  },
  
  async getProfile(token) {
    const response = await axios.get(`${API_BASE.userManagement}/auth/profile`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  }
};

// User service
export const userService = {
  async getUser(userId) {
    const response = await axios.get(`${API_BASE.userManagement}/users/${userId}`);
    return response.data;
  },
  
  async getUsersByDepartment(department) {
    const response = await axios.get(`${API_BASE.userManagement}/users/department/${department}`);
    return response.data;
  }
};

// Recommendations service
export const recommendationsService = {
  async getRecommendations(userId) {
    const response = await axios.get(`${API_BASE.recommendations}/recommendations/${userId}`);
    return response.data;
  },
  
  async getCourseRecommendations(userId) {
    const response = await axios.get(`${API_BASE.recommendations}/recommendations/courses/${userId}`);
    return response.data;
  },
  
  async getMentorRecommendations(userId) {
    const response = await axios.get(`${API_BASE.recommendations}/recommendations/mentors/${userId}`);
    return response.data;
  }
};
```

### Pinia Store Example

```javascript
// stores/auth.js
import { defineStore } from 'pinia';
import { authService } from '@/services/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),
  
  actions: {
    async login(email, password) {
      try {
        const response = await authService.login(email, password);
        this.token = response.data.token;
        this.user = response.data.user;
        this.isAuthenticated = true;
        localStorage.setItem('token', this.token);
        return response;
      } catch (error) {
        throw error;
      }
    },
    
    async getProfile() {
      try {
        const response = await authService.getProfile(this.token);
        this.user = response.data.user;
        return response;
      } catch (error) {
        this.logout();
        throw error;
      }
    },
    
    logout() {
      this.user = null;
      this.token = null;
      this.isAuthenticated = false;
      localStorage.removeItem('token');
    }
  }
});
```

### Component Examples

```vue
<!-- Login.vue -->
<template>
  <div class="login-form">
    <form @submit.prevent="handleLogin">
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit" :disabled="loading">Login</button>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';

export default {
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: null
    };
  },
  
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;
      
      try {
        await this.authStore.login(this.email, this.password);
        this.$router.push('/dashboard');
      } catch (error) {
        this.error = error.response?.data?.Message || 'Login failed';
      } finally {
        this.loading = false;
      }
    }
  },
  
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  }
};
</script>
```

```vue
<!-- Dashboard.vue -->
<template>
  <div class="dashboard">
    <div class="user-profile">
      <h1>Welcome, {{ user?.name }}</h1>
      <p>{{ user?.job_title }} - {{ user?.department }}</p>
    </div>
    
    <div class="recommendations">
      <h2>Recommendations</h2>
      <div v-for="rec in recommendations" :key="rec.type" class="recommendation-card">
        <h3>{{ rec.title }}</h3>
        <p>{{ rec.description }}</p>
        <span class="match-score">{{ rec.match_score }}% match</span>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '@/stores/auth';
import { recommendationsService } from '@/services/api';

export default {
  data() {
    return {
      recommendations: []
    };
  },
  
  computed: {
    user() {
      return this.authStore.user;
    }
  },
  
  async mounted() {
    await this.loadRecommendations();
  },
  
  methods: {
    async loadRecommendations() {
      try {
        const response = await recommendationsService.getRecommendations(this.user.id);
        this.recommendations = response.data.recommendations;
      } catch (error) {
        console.error('Failed to load recommendations:', error);
      }
    }
  },
  
  setup() {
    const authStore = useAuthStore();
    return { authStore };
  }
};
</script>
```

## 🧪 Testing

### Manual Testing Commands

```bash
# Test login
curl -X POST http://localhost:5001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"samantha.lee@globalpsa.com","password":"demo123"}'

# Test user profile
curl http://localhost:5001/users/EMP-20001

# Test recommendations
curl http://localhost:5004/recommendations/EMP-20001
```

### Automated Testing

```bash
# Run the test script
cd backend
python3 test_endpoints.py
```

## 📋 Demo User Accounts

| Email | Password | Employee ID | Name | Job Title |
|-------|----------|-------------|------|-----------|
| samantha.lee@globalpsa.com | demo123 | EMP-20001 | Samantha Lee | Cloud Solutions Architect |
| aisyah.rahman@globalpsa.com | demo123 | EMP-20002 | Nur Aisyah Binte Rahman | Cybersecurity Analyst |
| rohan.mehta@globalpsa.com | demo123 | EMP-20003 | Rohan Mehta | Finance Manager (FP&A) |

## ⚠️ Important Notes

### Database Setup Required
- The demo users need to be added to your Supabase database
- See `SETUP_GUIDE.md` for database setup instructions
- Currently, the API returns errors because demo users don't exist in the database

### Row Level Security (RLS)
- Supabase RLS policies may prevent data insertion
- You may need to disable RLS or configure policies for testing
- Contact your database administrator for RLS configuration

### CORS Configuration
- Services are configured to allow all origins (`*`)
- This is suitable for development but should be restricted in production

## 🔧 Troubleshooting

### Service Not Starting
```bash
# Check if ports are available
lsof -i :5001
lsof -i :5004

# Kill existing processes
pkill -f "python3 app.py"
```

### Database Connection Issues
- Verify Supabase connection settings in `.env` file
- Check if Supabase project is active
- Ensure API keys are correct

### Authentication Issues
- Verify JWT secret in `.env` file
- Check token expiration settings
- Ensure user exists in database

## 📞 Support

For technical issues:
1. Check the `API.md` documentation
2. Run the test script to verify functionality
3. Check service logs for error details
4. Verify database connection and data

## 🎯 Next Steps

1. **Database Setup**: Add demo users to Supabase database
2. **Frontend Integration**: Use the provided examples to integrate with your Vue.js frontend
3. **Testing**: Test all endpoints with the provided test script
4. **Customization**: Modify recommendation algorithms and add more demo data as needed

The backend services are ready and the API documentation is comprehensive. The main requirement is setting up the demo data in your Supabase database to enable full functionality.
