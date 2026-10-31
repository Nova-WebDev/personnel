import { create } from "zustand";

import type { Meal } from "../types";

interface MealState {
  meals: Record<string, Meal>;
  isComplete: boolean;
  setAll: (list: Meal[]) => void;
  upsert: (meal: Meal) => void;
  remove: (id: string) => void;
  invalidate: () => void;
}

export const useMealStore = create<MealState>((set) => ({
  meals: {},
  isComplete: false,
  setAll: (list) =>
    set({
      meals: Object.fromEntries(list.map((meal) => [meal.id, meal])),
      isComplete: true,
    }),
  upsert: (meal) =>
    set((state) => ({ meals: { ...state.meals, [meal.id]: meal } })),
  remove: (id) =>
    set((state) => {
      const meals = { ...state.meals };
      delete meals[id];
      return { meals };
    }),
  invalidate: () => set({ isComplete: false }),
}));
