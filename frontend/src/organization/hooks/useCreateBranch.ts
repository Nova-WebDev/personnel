import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createBranch } from "../api";
import { useOrganizationStore } from "../store/useOrganizationStore";

export function useCreateBranch() {
  const queryClient = useQueryClient();
  const invalidate = useOrganizationStore((state) => state.invalidate);

  return useMutation({
    mutationFn: (name: string) => createBranch(name),
    onSuccess: async () => {
      invalidate();
      await queryClient.invalidateQueries({ queryKey: ["branches"] });
    },
  });
}
