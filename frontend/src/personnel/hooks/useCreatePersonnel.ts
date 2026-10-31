import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createPersonnel } from "../api";
import { usePersonnelStore } from "../store/usePersonnelStore";
import type { CreatePersonnelInput } from "../types";

export function useCreatePersonnel() {
  const queryClient = useQueryClient();
  const invalidate = usePersonnelStore((state) => state.invalidate);

  return useMutation({
    mutationFn: (input: CreatePersonnelInput) => createPersonnel(input),
    onSuccess: async () => {
      invalidate();
      await queryClient.invalidateQueries({ queryKey: ["personnel"] });
    },
  });
}
