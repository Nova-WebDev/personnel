import type { SseEnvelope } from "./index";

export function handleSystemEvent(envelope: SseEnvelope): void {
  if (envelope.event === "system.error") {
    console.error("[system.error]", envelope.data);
  }
}
