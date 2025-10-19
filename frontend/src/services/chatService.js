// services/chatService.js
import api from './api.js'

export const chatService = {
  async sendMessage(message, userId) {
    try {
      const response = await api.post('/api/chat/message', {
        message,
        user_id: userId
      })
      
      return {
        success: true,
        response: response.data.data.response
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.Message || 'Failed to send message'
      }
    }
  }
}
