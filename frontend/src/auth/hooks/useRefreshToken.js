import { useMutation } from "@tanstack/react-query";
import { refreshToken } from "../../auth/api/authApi";

export function useRefreshToken() {
  return useMutation({
    mutationFn: ({ refresh_token }) => refreshToken(refresh_token),
  });
}
