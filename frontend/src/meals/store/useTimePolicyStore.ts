import { create } from "zustand";

import type { TimePolicy } from "../types";

interface TimePolicyState {
  policies: TimePolicy[];
  isComplete: boolean;
  setPolicies: (policies: TimePolicy[]) => void;
  invalidate: () => void;
}

export const useTimePolicyStore = create<TimePolicyState>((set) => ({
  policies: [],
  isComplete: false,
  setPolicies: (policies) => set({ policies, isComplete: true }),
  invalidate: () => set({ isComplete: false }),
}));
