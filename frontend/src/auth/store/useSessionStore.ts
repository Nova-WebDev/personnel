import { create } from "zustand";

export type SessionStatus = "unknown" | "authenticated" | "anonymous";

interface SessionState {
  status: SessionStatus;
  setStatus: (status: SessionStatus) => void;
}

export const useSessionStore = create<SessionState>((set) => ({
  status: "unknown",
  setStatus: (status) => set({ status }),
}));
