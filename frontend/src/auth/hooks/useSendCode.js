import { useMutation } from "@tanstack/react-query";
import { sendCode } from "../../auth/api/authApi";

export function useSendCode() {
  return useMutation({
    mutationFn: ({ phone_number }) => sendCode(phone_number),
  });
}
