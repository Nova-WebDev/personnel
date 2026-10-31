import { useMutation, useQueryClient } from "@tanstack/react-query";

import { createMeal } from "../api";
import { useMealStore } from "../store/useMealStore";
import type { CreateMealInput } from "../types";

export function useCreateMeal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: CreateMealInput) => createMeal(input),
    onSuccess: async () => {
      useMealStore.getState().invalidate();
      await queryClient.invalidateQueries({ queryKey: ["meals"] });
    },
  });
}
