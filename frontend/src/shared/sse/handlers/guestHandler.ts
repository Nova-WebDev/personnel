import { queryClient } from "../../../app/queryClient";
import type { SseEnvelope } from "./index";

export function handleGuestEvent(envelope: SseEnvelope): void {
  if (envelope.event.startsWith("guest.")) {
    void queryClient.invalidateQueries({ queryKey: ["day-report"] });
  }
}
