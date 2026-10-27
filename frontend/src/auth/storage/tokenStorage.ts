export const REFRESH_KEY = "refresh_token";
const EXPIRES_KEY = "access_token_expires_at";

export const tokenStorage = {
  getRefreshToken(): string | null {
    return localStorage.getItem(REFRESH_KEY);
  },

  getExpiresAt(): number | null {
    const value = Number(localStorage.getItem(EXPIRES_KEY));
    return Number.isFinite(value) && value > 0 ? value : null;
  },

  save(refreshToken: string, expiresAt: number): void {
    localStorage.setItem(REFRESH_KEY, refreshToken);
    localStorage.setItem(EXPIRES_KEY, String(expiresAt));
  },

  clear(): void {
    localStorage.removeItem(REFRESH_KEY);
    localStorage.removeItem(EXPIRES_KEY);
  },
};
