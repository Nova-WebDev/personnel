import { handleGuestEvent } from "./guestHandler";
import { handleMealEvent } from "./mealHandler";
import { handleMealPlanEvent } from "./mealPlanHandler";
import { handleSystemEvent } from "./systemHandler";
import { handleUserEvent } from "./userHandler";
import { handleVoucherEvent } from "./voucherHandler";
import { handleOrganizationEvent } from "./organizationHandler";
import { handlePermissionEvent } from "./permissionHandler";

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
  branch: handleOrganizationEvent,
  unit: handleOrganizationEvent,
  permission: handlePermissionEvent,
};

export function dispatchSseEvent(envelope: SseEnvelope): void {
  const handler = handlersByScope[envelope.scope];
  console.log(
    "[dispatch]",
    envelope.scope,
    handler === undefined ? "NO HANDLER" : "ok",
  );
  handler?.(envelope);
}
