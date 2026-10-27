import { queryClient } from "../../../app/queryClient";
import type { SseEnvelope } from "./index";

export function handleMealPlanEvent(envelope: SseEnvelope): void {
  switch (envelope.event) {
    case "meal_plan.created":
    case "meal_plan.updated":
    case "meal_plan.deleted":
    case "meal_plan.recurring_applied":
      void queryClient.invalidateQueries({ queryKey: ["meal-plans"] });
      break;
    case "meal_plan.recurring_cycle_updated":
      void queryClient.invalidateQueries({ queryKey: ["meal-plan-recurring"] });
      break;
  }
}
