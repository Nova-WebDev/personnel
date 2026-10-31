import { useMutation, useQueryClient } from "@tanstack/react-query";

import { updatePersonnel } from "../api";
import { usePersonnelStore } from "../store/usePersonnelStore";
import type { CreatePersonnelInput } from "../types";

export function useUpdatePersonnel() {
  const queryClient = useQueryClient();
  const invalidate = usePersonnelStore((state) => state.invalidate);

  return useMutation({
    mutationFn: ({ id, input }: { id: string; input: CreatePersonnelInput }) =>
      updatePersonnel(id, input),
    onSuccess: async () => {
      invalidate();
      await queryClient.invalidateQueries({ queryKey: ["personnel"] });
    },
  });
}
