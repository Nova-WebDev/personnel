import axios from "axios";

import { refreshToken } from "../api";
import { tokenStorage } from "./tokenStorage";

export type RefreshResult = "ok" | "rejected" | "network_error";

const LOCK_NAME = "session-refresh";
const SKIP_IF_REMAINING_SECONDS = 120;
const REJECTING_STATUSES = new Set([401, 403]);

function nowSeconds(): number {
  return Math.floor(Date.now() / 1000);
}

async function execute(force: boolean): Promise<RefreshResult> {
  const stored = tokenStorage.getRefreshToken();
  if (stored === null) return "rejected";

  const expiresAt = tokenStorage.getExpiresAt();
  if (
    !force &&
    expiresAt !== null &&
    expiresAt - nowSeconds() > SKIP_IF_REMAINING_SECONDS
  ) {
    return "ok";
  }

  try {
    const { data } = await refreshToken(stored);
    tokenStorage.save(data.refresh_token, data.access_token_expires_at);
    return "ok";
  } catch (error) {
    if (
      axios.isAxiosError(error) &&
      error.response !== undefined &&
      REJECTING_STATUSES.has(error.response.status)
    ) {
      return "rejected";
    }
    return "network_error";
  }
}

export function requestRefresh(force: boolean): Promise<RefreshResult> {
  if (typeof navigator.locks === "undefined") return execute(force);
  return navigator.locks.request(LOCK_NAME, () => execute(force));
}
