import { handleGuestEvent } from "./guestHandler";
import { handleMealEvent } from "./mealHandler";
import { handleMealPlanEvent } from "./mealPlanHandler";
import { handleSystemEvent } from "./systemHandler";
import { handleUserEvent } from "./userHandler";
import { handleVoucherEvent } from "./voucherHandler";

export interface SseEnvelope {
  event: string;
  scope: string;
  meta: Record<string, unknown>;
  data: unknown;
}

export type SseHandler = (envelope: SseEnvelope) => void;

const handlersByScope: Record<string, SseHandler> = {
  meal: handleMealEvent,
  meal_plan: handleMealPlanEvent,
  voucher: handleVoucherEvent,
  guest: handleGuestEvent,
  user: handleUserEvent,
  system: handleSystemEvent,
};

export function dispatchSseEvent(envelope: SseEnvelope): void {
  handlersByScope[envelope.scope]?.(envelope);
}
