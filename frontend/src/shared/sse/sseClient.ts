import { queryClient } from "../../app/queryClient";
import { dispatchSseEvent, type SseEnvelope } from "./handlers";

const EVENTS_URL = "/events";

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
    console.debug("[sse] open");
    if (hasOpened) {
      void queryClient.invalidateQueries();
    }
    hasOpened = true;
  };

  stream.onmessage = (message: MessageEvent<string>) => {
    console.debug("[sse] message", message.data);
    const envelope = parseEnvelope(message.data);
    if (envelope !== null) {
      dispatchSseEvent(envelope);
    }
  };

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
