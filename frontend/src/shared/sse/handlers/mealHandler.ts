import { queryClient } from "../../../app/queryClient";
import { useMealStore } from "../../../meals/store/useMealStore";
import type { Meal } from "../../../meals/types";
import type { SseEnvelope } from "./index";

function isMeal(value: unknown): value is Meal {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "title" in value &&
    "is_active" in value
  );
}

function refetchMeals(): void {
  useMealStore.getState().invalidate();
  void queryClient.invalidateQueries({ queryKey: ["meals"] });
}

export function handleMealEvent(envelope: SseEnvelope): void {
  const { event, data } = envelope;
  const store = useMealStore.getState();

  if (event.startsWith("meal.")) {
    if (isMeal(data)) store.upsert(data);
    else refetchMeals();
    void queryClient.invalidateQueries({ queryKey: ["meal-plans"] });
  }
}
