import { useMutation } from "@tanstack/react-query";

import { setMealActive } from "../api";
import { useMealStore } from "../store/useMealStore";

export function useSetMealActive() {
  return useMutation({
    mutationFn: ({ id, isActive }: { id: string; isActive: boolean }) =>
      setMealActive(id, isActive),
    onSuccess: (_data, { id, isActive }) => {
      const { meals, upsert } = useMealStore.getState();
      const meal = meals[id];
      if (meal !== undefined) upsert({ ...meal, is_active: isActive });
    },
  });
}
