// store/chat.js
import { defineStore } from "pinia";

export const useChatStore = defineStore("chat", {
  state: () => ({
    messages: [
      {
        id: 1,
        type: "ai",
        content:
          "Hi! I'm here to help with your career development. What would you like to discuss today?",
        timestamp: new Date(),
      },
    ],
    isLoading: false,

    // right-panel state
    lastPlan: null,
    lastLeadership: null,
    lastFeedback: null,
  }),

  actions: {
    addMessage(message) {
      this.messages.push({
        id: Date.now(),
        timestamp: new Date(),
        ...message,
      });
    },

    clearMessages() {
      this.messages = [
        {
          id: 1,
          type: "ai",
          content:
            "Hi! I'm here to help with your career development. What would you like to discuss today?",
          timestamp: new Date(),
        },
      ];
      this.lastPlan = null;
      this.lastLeadership = null;
      this.lastFeedback = null;
    },

    setLoading(v) {
      this.isLoading = v;
    },

    setLastPlan(p) {
      this.lastPlan = p || null;
    },
    setLastLeadership(l) {
      this.lastLeadership = l || null;
    },
    setLastFeedback(f) {
      this.lastFeedback = f || null;
    },
  },
});
