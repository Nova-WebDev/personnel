import { queryClient } from "../../../app/queryClient";
import type { SseEnvelope } from "./index";

export function handleVoucherEvent(envelope: SseEnvelope): void {
  if (envelope.event.startsWith("voucher.")) {
    void queryClient.invalidateQueries({ queryKey: ["meal-plans"] });
    void queryClient.invalidateQueries({ queryKey: ["day-report"] });
  }
}
