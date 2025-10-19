import api from "./api.js";

export const chatService = {
  async sendMessage(message, userId = 1) {
    const res = await api.post("/chat/guidance", { user_id: userId, message });
    const data = res.data?.data || {};

    // data contains: reply, summary, plan, leadership, feedback, alternatives
    return {
      success: true,
      responseText: data.reply || data.summary || "(no reply)",
      payload: data,
    };
  },

  async getHealth() {
    const res = await api.get("/chat/health");
    return res.data;
  },
};
