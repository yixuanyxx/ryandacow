// store/chat.js
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [
      {
        id: 1,
        type: 'ai',
        content: "Hi! I'm here to help with your career development. What would you like to discuss today?",
        timestamp: new Date()
      }
    ],
    isLoading: false
  }),
  
  actions: {
    addMessage(message) {
      this.messages.push({
        id: Date.now(),
        timestamp: new Date(),
        ...message
      })
    },
    
    clearMessages() {
      this.messages = [
        {
          id: 1,
          type: 'ai',
          content: "Hi! I'm here to help with your career development. What would you like to discuss today?",
          timestamp: new Date()
        }
      ]
    },
    
    setLoading(loading) {
      this.isLoading = loading
    }
  }
})
