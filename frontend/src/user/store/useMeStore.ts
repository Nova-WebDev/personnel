import { create } from "zustand";

import type { Me } from "../types";

interface MeState {
  me: Me | null;
  setMe: (me: Me) => void;
  clear: () => void;
}

export const useMeStore = create<MeState>((set) => ({
  me: null,
  setMe: (me) => set({ me }),
  clear: () => set({ me: null }),
}));
