import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createUnit } from "../api";
import { useOrganizationStore } from "../store/useOrganizationStore";

interface CreateUnitInput {
  name: string;
  branchId: string;
}

export function useCreateUnit() {
  const queryClient = useQueryClient();
  const invalidate = useOrganizationStore((state) => state.invalidate);

  return useMutation({
    mutationFn: ({ name, branchId }: CreateUnitInput) =>
      createUnit(name, branchId),
    onSuccess: async () => {
      invalidate();
      await queryClient.invalidateQueries({ queryKey: ["branches"] });
    },
  });
}
