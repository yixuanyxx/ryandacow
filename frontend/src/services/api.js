// services/api.js
import axios from 'axios'

// Create axios instance with base configuration
const BASE = import.meta.env.VITE_AI_BASE || "http://localhost:5002";
console.log("[API Base URL]", BASE);

const api = axios.create({
  baseURL: BASE, // 👈 ensures calls go to port 5002
  withCredentials: false,
  timeout: 60000,
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api