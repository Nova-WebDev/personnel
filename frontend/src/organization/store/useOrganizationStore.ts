import { create } from "zustand";

import type { Branch } from "../types";

interface OrganizationState {
  branches: Branch[];
  isComplete: boolean;
  setBranches: (branches: Branch[]) => void;
  invalidate: () => void;
}

export const useOrganizationStore = create<OrganizationState>((set) => ({
  branches: [],
  isComplete: false,
  setBranches: (branches) => set({ branches, isComplete: true }),
  invalidate: () => set({ isComplete: false }),
}));
