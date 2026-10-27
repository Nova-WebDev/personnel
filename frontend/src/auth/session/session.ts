import { queryClient } from "../../app/queryClient";
import { sseClient } from "../../shared/sse/sseClient";
import { useSessionStore } from "../store/useSessionStore";
import { requestRefresh, type RefreshResult } from "./refresh";
import { REFRESH_KEY, tokenStorage } from "./tokenStorage";

const REFRESH_MARGIN_SECONDS = 60;
const BACKOFF_BASE_MS = 5_000;
const BACKOFF_MAX_MS = 60_000;
const RECOVER_JITTER_MS = 3_000;
const RECOVER_MIN_INTERVAL_MS = 10_000;

let refreshTimer: number | undefined;
let inflight: Promise<RefreshResult> | null = null;
let bootstrapPromise: Promise<void> | null = null;
let listenersAttached = false;
let failureCount = 0;
let blockedUntil = 0;
let lastRecoverAt = 0;

function nowSeconds(): number {
  return Math.floor(Date.now() / 1000);
}

function jitter(maxMs: number): number {
  return Math.floor(Math.random() * maxMs);
}

function isAuthenticated(): boolean {
  return useSessionStore.getState().status === "authenticated";
}

function scheduleIn(delayMs: number): void {
  window.clearTimeout(refreshTimer);
  refreshTimer = window.setTimeout(runScheduled, delayMs);
}

function scheduleAt(expiresAt: number): void {
  scheduleIn(
    Math.max(0, (expiresAt - REFRESH_MARGIN_SECONDS) * 1000 - Date.now()),
  );
}

function runScheduled(): void {
  blockedUntil = 0;
  void refreshSession();
}

function registerFailure(): void {
  failureCount += 1;
  const ceiling = Math.min(
    BACKOFF_MAX_MS,
    BACKOFF_BASE_MS * 2 ** (failureCount - 1),
  );
  const delay = ceiling / 2 + jitter(ceiling / 2);
  blockedUntil = Date.now() + delay;
  scheduleIn(delay);
}

function activate(expiresAt: number): void {
  failureCount = 0;
  blockedUntil = 0;
  useSessionStore.getState().setStatus("authenticated");
  sseClient.connect();
  scheduleAt(expiresAt);
}

function settle(result: RefreshResult): RefreshResult {
  if (result === "ok") {
    const expiresAt = tokenStorage.getExpiresAt();
    if (expiresAt !== null) activate(expiresAt);
  } else if (result === "rejected") {
    endSession();
  } else {
    registerFailure();
  }
  return result;
}

export function refreshSession(force = false): Promise<RefreshResult> {
  if (inflight !== null) return inflight;
  if (Date.now() < blockedUntil) return Promise.resolve("network_error");

  inflight = requestRefresh(force)
    .then(settle)
    .finally(() => {
      inflight = null;
    });
  return inflight;
}

async function recoverStream(): Promise<void> {
  await new Promise((resolve) =>
    window.setTimeout(resolve, jitter(RECOVER_JITTER_MS)),
  );
  if (!isAuthenticated() || Date.now() < blockedUntil) return;

  const now = Date.now();
  const tooSoon = now - lastRecoverAt < RECOVER_MIN_INTERVAL_MS;
  lastRecoverAt = now;

  if (tooSoon) {
    registerFailure();
    return;
  }
  await refreshSession(true);
}

function refreshIfDue(): void {
  if (!isAuthenticated() || Date.now() < blockedUntil) return;
  const expiresAt = tokenStorage.getExpiresAt();
  if (
    expiresAt === null ||
    expiresAt - nowSeconds() <= REFRESH_MARGIN_SECONDS
  ) {
    void refreshSession();
  }
}

function attachListeners(): void {
  if (listenersAttached) return;
  listenersAttached = true;

  sseClient.onClosed(() => void recoverStream());

  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "visible") refreshIfDue();
  });

  window.addEventListener("online", () => {
    blockedUntil = 0;
    refreshIfDue();
  });

  window.addEventListener("storage", (event) => {
    if (event.key === REFRESH_KEY && event.newValue === null) endSession();
  });
}

export function startSession(
  refreshTokenValue: string,
  expiresAt: number,
): void {
  attachListeners();
  tokenStorage.save(refreshTokenValue, expiresAt);
  activate(expiresAt);
}

export function endSession(): void {
  window.clearTimeout(refreshTimer);
  refreshTimer = undefined;
  failureCount = 0;
  blockedUntil = 0;
  sseClient.disconnect();
  tokenStorage.clear();
  queryClient.clear();
  useSessionStore.getState().setStatus("anonymous");
}

async function bootstrap(): Promise<void> {
  attachListeners();

  if (tokenStorage.getRefreshToken() === null) {
    useSessionStore.getState().setStatus("anonymous");
    return;
  }

  const expiresAt = tokenStorage.getExpiresAt();
  if (expiresAt !== null && expiresAt - nowSeconds() > REFRESH_MARGIN_SECONDS) {
    activate(expiresAt);
    return;
  }

  const result = await refreshSession();
  if (result === "network_error") {
    useSessionStore.getState().setStatus("authenticated");
  }
}

export function bootstrapSession(): Promise<void> {
  bootstrapPromise ??= bootstrap();
  return bootstrapPromise;
}
