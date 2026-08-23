import { create } from "zustand";

export const useTempPhoneStore = create((set) => ({
  tempPhone: null,
  setTempPhone: (phone) =>
    set({
      tempPhone: phone,
    }),
  clearTempPhone: () =>
    set({
      tempPhone: null,
    }),
}));
