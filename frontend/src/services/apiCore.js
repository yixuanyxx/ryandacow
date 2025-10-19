import axios from "axios";

const BASE = import.meta.env.VITE_API_BASE || "http://localhost:5001";

const apiCore = axios.create({
  baseURL: BASE,
  withCredentials: false,
  timeout: 15000,
});

apiCore.interceptors.request.use((config) => {
    const isLogin = (config.url || '').includes('/auth/login');
    if (!isLogin) {
        const token = localStorage.getItem("token");
        if (token) config.headers.Authorization = `Bearer ${token}`;
    }
  return config;
});

export default apiCore;