import api from "../../shared/lib/axios";

export function sendCode(phoneNumber) {
  return api.post("/auth/send-code", { phone_number: phoneNumber });
}

export function verifyCode(phoneNumber, code) {
  return api.post("/auth/verify-code/", { phone_number: phoneNumber, code });
}

export function refreshToken(refreshToken) {
  return api.post("/auth/refresh/", { refresh_token: refreshToken });
}

export function logout(refreshToken) {
  return api.post("/auth/log-out/", { refresh_token: refreshToken });
}
