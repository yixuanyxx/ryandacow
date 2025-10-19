// store/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: null,
    isAuthenticated: false
  }),
  
  actions: {
    login(userData, token) {
      this.user = userData
      this.token = token
      this.isAuthenticated = true
      
      // Store in localStorage for persistence
      localStorage.setItem('user', JSON.stringify(userData))
      localStorage.setItem('token', token)
    },
    
    logout() {
      this.user = null
      this.token = null
      this.isAuthenticated = false
      
      // Clear localStorage
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    },
    
    // Initialize from localStorage on app start
    initializeAuth() {
      const user = localStorage.getItem('user')
      const token = localStorage.getItem('token')
      
      if (user && token) {
        this.user = JSON.parse(user)
        this.token = token
        this.isAuthenticated = true
      }
    }
  }
})
