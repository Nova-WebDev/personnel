import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  withCredentials: true,
  timeout: 30_000,
  headers: { "Content-Type": "application/json" },
});

export default api;
