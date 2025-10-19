import axios from "axios";
const BASE = import.meta.env.VITE_RECS_BASE || "http://localhost:5004";
const apiRecs = axios.create({ baseURL: BASE, withCredentials: false, timeout: 20000 });
export default apiRecs;