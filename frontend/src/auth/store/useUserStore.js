import { create } from "zustand";

export const useUserStore = create((set) => ({
  phone_number: null,
  public_id: null,
  role: null,
  exp: null,
  setUserFromToken: (decoded) =>
    set({
      phone_number: decoded.phone_number,
      public_id: decoded.public_id,
      role: decoded.role,
      exp: decoded.exp,
    }),
  clearUser: () =>
    set({
      phone_number: null,
      public_id: null,
      role: null,
      exp: null,
    }),
}));
