
import axios from "axios";

const origin = window.location.origin;

const axiosMultipart = axios.create({
  baseURL: `${origin}/api`,
  withCredentials: true,
});

export default axiosMultipart;
