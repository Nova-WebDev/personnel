import { queryClient } from "../../../app/queryClient";
import type { SseEnvelope } from "./index";

export function handleMealEvent(envelope: SseEnvelope): void {
  if (envelope.event.startsWith("meal.")) {
    void queryClient.invalidateQueries({ queryKey: ["meals"] });
    void queryClient.invalidateQueries({ queryKey: ["meal-plans"] });
  }
}
