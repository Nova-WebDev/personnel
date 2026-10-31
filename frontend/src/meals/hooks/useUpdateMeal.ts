import { useMutation, useQueryClient } from "@tanstack/react-query";

import { updateMeal } from "../api";
import { useMealStore } from "../store/useMealStore";
import type { CreateMealInput } from "../types";

export function useUpdateMeal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, input }: { id: string; input: CreateMealInput }) =>
      updateMeal(id, input),
    onSuccess: async () => {
      useMealStore.getState().invalidate();
      await queryClient.invalidateQueries({ queryKey: ["meals"] });
    },
  });
}
