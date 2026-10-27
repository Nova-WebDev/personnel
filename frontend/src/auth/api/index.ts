import api from "../../shared/lib/axios";

export interface TokenResponse {
  refresh_token: string;
  access_token_expires_at: number;
}

export function sendCode(phoneNumber: string) {
  return api.post("/auth/send-code", { phone_number: phoneNumber });
}

export function verifyCode(phoneNumber: string, code: string) {
  return api.post<TokenResponse>("/auth/verify-code", {
    phone_number: phoneNumber,
    code,
  });
}

export function refreshToken(token: string) {
  return api.post<TokenResponse>("/auth/refresh", { refresh_token: token });
}

export function logout(token: string) {
  return api.post("/auth/log-out", { refresh_token: token });
}
