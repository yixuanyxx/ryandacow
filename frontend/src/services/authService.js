// services/authService.js
import api from './api.js'

export const authService = {
  async login(email, password) {
    try {
      const response = await api.post('/api/auth/login', {
        email,
        password
      })
      
      if (response.data.Message === 'Login successful') {
        return {
          success: true,
          user: response.data.data.user,
          token: response.data.data.token
        }
      } else {
        return {
          success: false,
          error: response.data.Message || 'Login failed'
        }
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.Message || 'Login failed. Please try again.'
      }
    }
  },

  async getProfile() {
    try {
      const response = await api.get('/api/auth/profile')
      return {
        success: true,
        data: response.data.data
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.Message || 'Failed to get profile'
      }
    }
  }
}
