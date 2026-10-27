import { useMutation } from "@tanstack/react-query";

import { logout } from "../api";
import { endSession, tokenStorage } from "../session";

export function useLogout() {
  return useMutation({
    mutationFn: async () => {
      const token = tokenStorage.getRefreshToken();
      if (token !== null) await logout(token);
    },
    onSettled: () => {
      endSession();
    },
  });
}
