import { create } from "zustand";

interface TimeState {
  offsetMs: number;
  isComplete: boolean;
  setServerTime: (serverIso: string) => void;
}

export const useTimeStore = create<TimeState>((set) => ({
  offsetMs: 0,
  isComplete: false,
  setServerTime: (serverIso) =>
    set({
      offsetMs: new Date(serverIso).getTime() - Date.now(),
      isComplete: true,
    }),
}));

export function serverNow(): number {
  return Date.now() + useTimeStore.getState().offsetMs;
}
