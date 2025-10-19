import axios from "axios";
const BASE = import.meta.env.VITE_AI_BASE || "http://localhost:5002";
const apiAI = axios.create({ baseURL: BASE, withCredentials: false, timeout: 20000 });
export default apiAI;