import { create } from "zustand";

import type { MealPlan } from "../types";

interface MealPlanState {
  plans: Record<string, MealPlan>;
  loadedFrom: string | null;
  loadedTo: string | null;
  isComplete: boolean;
  setRange: (plans: MealPlan[], from: string, to: string) => void;
  upsert: (plan: MealPlan) => void;
  remove: (planId: string) => void;
  setReserved: (planId: string, reserved: boolean) => void;
  invalidate: () => void;
}

export const useMealPlanStore = create<MealPlanState>((set) => ({
  plans: {},
  loadedFrom: null,
  loadedTo: null,
  isComplete: false,
  setRange: (list, from, to) =>
    set({
      plans: Object.fromEntries(list.map((plan) => [plan.id, plan])),
      loadedFrom: from,
      loadedTo: to,
      isComplete: true,
    }),
  upsert: (plan) =>
    set((state) => ({ plans: { ...state.plans, [plan.id]: plan } })),
  remove: (planId) =>
    set((state) => {
      const { [planId]: _removed, ...rest } = state.plans;
      return { plans: rest };
    }),
  setReserved: (planId, reserved) =>
    set((state) => {
      const plan = state.plans[planId];
      return plan === undefined
        ? state
        : {
            plans: {
              ...state.plans,
              [planId]: { ...plan, is_reserved: reserved },
            },
          };
    }),
  invalidate: () => set({ isComplete: false }),
}));
