// services/chatService.js
import api from './api.js';

export const chatService = {
  async sendMessage(message, userId = 1) {
    try {
      const res = await api.post("/chat/guidance", { user_id: userId, message });
      const data = res.data?.data || {};
      return { success: true, responseText: data.reply || data.summary || "", payload: data };
    } catch (error) {
      // Friendlier frontend error for timeouts
      const isTimeout = error.code === "ECONNABORTED" || /timeout/i.test(error.message || "");
      const msg = isTimeout
        ? "The AI took too long to respond. I’ll try to be snappier next time."
        : (error?.response?.data?.Message || "Failed to send message");
      return { success: false, error: msg };
    }
  },

  async getHealth() {
    const res = await api.get('/chat/health');
    return res.data;
  },
};