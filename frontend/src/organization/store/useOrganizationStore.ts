import { create } from "zustand";

import type { Branch } from "../types";

export interface UnitInfo {
  unitName: string;
  branchId: string;
  branchName: string;
}

interface OrganizationState {
  branches: Branch[];
  unitLookup: Record<string, UnitInfo>;
  isComplete: boolean;
  setBranches: (branches: Branch[]) => void;
  addBranch: (id: string, name: string) => void;
  addUnit: (id: string, name: string, branchId: string) => void;
  invalidate: () => void;
}

function buildLookup(branches: Branch[]): Record<string, UnitInfo> {
  const lookup: Record<string, UnitInfo> = {};
  for (const branch of branches) {
    for (const unit of branch.units) {
      lookup[unit.unit_id] = {
        unitName: unit.unit_name,
        branchId: branch.branch_id,
        branchName: branch.branch_name,
      };
    }
  }
  return lookup;
}

export const useOrganizationStore = create<OrganizationState>((set) => ({
  branches: [],
  unitLookup: {},
  isComplete: false,
  setBranches: (branches) =>
    set({ branches, unitLookup: buildLookup(branches), isComplete: true }),
  addBranch: (id, name) =>
    set((state) => {
      if (state.branches.some((branch) => branch.branch_id === id))
        return state;
      const branches = [
        ...state.branches,
        { branch_id: id, branch_name: name, units: [] },
      ];
      return { branches, unitLookup: buildLookup(branches) };
    }),
  addUnit: (id, name, branchId) =>
    set((state) => {
      const branches = state.branches.map((branch) =>
        branch.branch_id !== branchId ||
        branch.units.some((unit) => unit.unit_id === id)
          ? branch
          : {
              ...branch,
              units: [...branch.units, { unit_id: id, unit_name: name }],
            },
      );
      return { branches, unitLookup: buildLookup(branches) };
    }),
  invalidate: () => set({ isComplete: false }),
}));
