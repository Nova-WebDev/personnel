import { useMutation, useQueryClient } from "@tanstack/react-query";

import { useTimePolicyStore } from "../../meals/store/useTimePolicyStore";
import { setTimePolicies, type TimePolicyInput } from "../api";

export function useSetTimePolicies() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (policies: TimePolicyInput[]) => setTimePolicies(policies),
    onSuccess: async () => {
      useTimePolicyStore.getState().invalidate();
      await queryClient.invalidateQueries({ queryKey: ["time-policies"] });
    },
  });
}
