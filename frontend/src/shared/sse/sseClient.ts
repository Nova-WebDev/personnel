import { queryClient } from "../../app/queryClient";
import { dispatchSseEvent, type SseEnvelope } from "./handlers";

const EVENTS_URL = "/events";

const EVENT_NAMES = [
  "branch.created",
  "branch.updated",
  "branch.deleted",
  "unit.created",
  "unit.updated",
  "unit.deleted",
  "user.created",
  "user.updated",
  "user.blocked_status_changed",
  "user.rfid_updated",
  "user.permissions_updated",
  "user.permissions_deleted",
  "meal.created",
  "meal.updated",
  "meal.active_status_changed",
  "meal_plan.created",
  "meal_plan.updated",
  "meal_plan.deleted",
  "meal_plan.recurring_applied",
  "meal_plan.recurring_cycle_updated",
  "voucher.reserved",
  "voucher.cancelled",
  "voucher.redeemed",
  "guest.updated",
  "system.error",
];

let source: EventSource | null = null;
let hasOpened = false;
let closedHandler: (() => void) | null = null;

function parseEnvelope(raw: string): SseEnvelope | null {
  try {
    const parsed: unknown = JSON.parse(raw);
    if (
      typeof parsed === "object" &&
      parsed !== null &&
      "event" in parsed &&
      "scope" in parsed
    ) {
      return parsed as SseEnvelope;
    }
    return null;
  } catch {
    return null;
  }
}

function closeSource(): void {
  if (source === null) return;
  source.onopen = null;
  source.onmessage = null;
  source.onerror = null;
  source.close();
  source = null;
}

function connect(): void {
  closeSource();

  const stream = new EventSource(EVENTS_URL);
  source = stream;

  stream.onopen = () => {
    console.log("[sse] open");
    if (hasOpened) {
      void queryClient.invalidateQueries();
    }
    hasOpened = true;
  };

  const handle = (message: MessageEvent<string>) => {
    console.log("[sse]", message.type, message.data);
    const envelope = parseEnvelope(message.data);
    if (envelope !== null) {
      dispatchSseEvent(envelope);
    }
  };

  stream.onmessage = handle;
  for (const name of EVENT_NAMES) {
    stream.addEventListener(name, handle as EventListener);
  }

  stream.onerror = () => {
    if (source !== stream) return;
    closeSource();
    closedHandler?.();
  };
}

function disconnect(): void {
  closeSource();
  hasOpened = false;
}

function onClosed(handler: () => void): void {
  closedHandler = handler;
}

export const sseClient = { connect, disconnect, onClosed };
