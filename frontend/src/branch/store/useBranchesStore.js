import { create } from "zustand";

export const useBranchesStore = create((set, get) => ({
  branches: [],
  isSet: false,

  setBranches: (list) =>
    set(() => ({
      branches: Array.isArray(list) ? [...list] : [],
      isSet: true,
    })),

  addBranch: (branch) =>
    set((state) => ({
      branches: [...state.branches, { ...branch, units: branch.units || [] }],
    })),

  removeBranch: (branchId) =>
    set((state) => ({
      branches: state.branches.filter((b) => b.id !== branchId),
    })),

  updateBranch: (branchId, patch) =>
    set((state) => ({
      branches: state.branches.map((b) =>
        b.id === branchId ? { ...b, ...patch } : b
      ),
    })),

  addUnit: (branchId, unit) =>
    set((state) => ({
      branches: state.branches.map((b) =>
        b.id === branchId
          ? { ...b, units: [...b.units, unit] }
          : b
      ),
    })),

  removeUnit: (branchId, unitId) =>
    set((state) => ({
      branches: state.branches.map((b) =>
        b.id === branchId
          ? { ...b, units: b.units.filter((u) => u.id !== unitId) }
          : b
      ),
    })),

  updateUnit: (branchId, unitId, patch) =>
    set((state) => ({
      branches: state.branches.map((b) =>
        b.id === branchId
          ? {
              ...b,
              units: b.units.map((u) =>
                u.id === unitId ? { ...u, ...patch } : u
              ),
            }
          : b
      ),
    })),
}));
