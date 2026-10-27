import { queryClient } from "../../../app/queryClient";
import type { SseEnvelope } from "./index";

export function handleUserEvent(envelope: SseEnvelope): void {
  if (envelope.event.startsWith("user.")) {
    void queryClient.invalidateQueries({ queryKey: ["users"] });
    void queryClient.invalidateQueries({ queryKey: ["me"] });
  }
}
