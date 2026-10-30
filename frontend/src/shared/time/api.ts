import api from "../lib/axios";

export function getServerTime() {
  return api.get<{ server_time: string }>("/app/time");
}
