import { useMutation } from "@tanstack/react-query";

import { sendCode } from "../api";

export function useSendCode() {
  return useMutation({
    mutationFn: (phoneNumber: string) => sendCode(phoneNumber),
  });
}
