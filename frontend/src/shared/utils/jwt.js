import { jwtDecode } from "jwt-decode";

export function decodeJWT(token) {
  try {
    return jwtDecode(token);
  } catch (err) {
    console.error("JWT decode error:", err);
    return null;
  }
}
