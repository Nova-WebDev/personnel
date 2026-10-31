import { create } from "zustand";

import { computeAccess } from "../permissions";
import type { Me } from "../types";

interface MeState {
  me: Me | null;
  isAdmin: boolean;
  hrUnitIds: Set<string> | null;
  setMe: (me: Me) => void;
  clear: () => void;
}

export const useMeStore = create<MeState>((set) => ({
  me: null,
  isAdmin: false,
  hrUnitIds: new Set<string>(),
  setMe: (me) => set({ me, ...computeAccess(me) }),
  clear: () => set({ me: null, isAdmin: false, hrUnitIds: new Set<string>() }),
}));
