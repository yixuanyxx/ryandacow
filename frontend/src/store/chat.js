// store/chat.js
import { defineStore } from 'pinia'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [
      { id: 1, type: 'ai', content: "Hi! I'm here to help with your career development. What would you like to discuss today?", timestamp: new Date() }
    ],
    isLoading: false,

    // 👉 right-panel widget data
    lastPlan: null,
    lastLeadership: null,
    lastFeedback: null,     // includes recommended_actions, next_questions, etc.
  }),

  actions: {
    addMessage(message) {
      this.messages.push({ id: Date.now(), timestamp: new Date(), ...message })
    },
    clearMessages() {
      this.messages = [this.messages[0]]
      this.lastPlan = null
      this.lastLeadership = null
      this.lastFeedback = null
    },
    setLoading(v) { this.isLoading = v },

    // called after /chat/guidance returns
    setFromGuidance({ plan, leadership, feedback }) {
      this.lastPlan = plan || null
      this.lastLeadership = leadership || null
      this.lastFeedback = feedback || null
    }
  }
})