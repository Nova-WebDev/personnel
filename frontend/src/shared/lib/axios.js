import axios from "axios";

const origin = window.location.origin;

const api = axios.create({
  baseURL: `${origin}/api`,
  withCredentials: true,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;