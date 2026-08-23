import { useMutation } from "@tanstack/react-query";
import { verifyCode } from "../../auth/api/authApi";

export function useVerifyCode() {
  return useMutation({
    mutationFn: ({ phone_number, code }) => verifyCode(phone_number, code),
  });
}
