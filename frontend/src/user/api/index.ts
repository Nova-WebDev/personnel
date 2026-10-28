import api from "../../shared/lib/axios";
import type { Me } from "../types";

export function getMe() {
  return api.get<Me>("/user/me");
}
