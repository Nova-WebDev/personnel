import { create } from "zustand";

import type { Permission } from "../types";

interface PermissionState {
  items: Record<string, Permission>;
  isComplete: boolean;
  setAll: (list: Permission[]) => void;
  upsert: (permission: Permission) => void;
  remove: (permissionId: string) => void;
  invalidate: () => void;
}

export const usePermissionStore = create<PermissionState>((set) => ({
  items: {},
  isComplete: false,
  setAll: (list) =>
    set({
      items: Object.fromEntries(list.map((item) => [item.permission_id, item])),
      isComplete: true,
    }),
  upsert: (permission) =>
    set((state) => ({
      items: { ...state.items, [permission.permission_id]: permission },
    })),
  remove: (permissionId) =>
    set((state) => {
      const items = { ...state.items };
      delete items[permissionId];
      return { items };
    }),
  invalidate: () => set({ isComplete: false }),
}));
