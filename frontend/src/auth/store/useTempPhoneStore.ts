import { create } from "zustand";

interface TempPhoneState {
  tempPhone: string;
  setTempPhone: (phone: string) => void;
  clearTempPhone: () => void;
}

export const useTempPhoneStore = create<TempPhoneState>((set) => ({
  tempPhone: "",
  setTempPhone: (tempPhone) => set({ tempPhone }),
  clearTempPhone: () => set({ tempPhone: "" }),
}));
