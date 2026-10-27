import { useMutation } from "@tanstack/react-query";

import { verifyCode } from "../api";
import { startSession } from "../session";

interface VerifyCodeInput {
  phoneNumber: string;
  code: string;
}

export function useVerifyCode() {
  return useMutation({
    mutationFn: async ({ phoneNumber, code }: VerifyCodeInput) => {
      const { data } = await verifyCode(phoneNumber, code);
      return data;
    },
    onSuccess: (data) => {
      startSession(data.refresh_token, data.access_token_expires_at);
    },
  });
}
