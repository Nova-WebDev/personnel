import axios from "axios";

const axiosMultipart = axios.create({
  baseURL: "/api",
  withCredentials: true,
  timeout: 60_000,
});

export default axiosMultipart;
