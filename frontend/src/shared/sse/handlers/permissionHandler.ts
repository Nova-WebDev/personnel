import { usePermissionStore } from "../../../access/store/usePermissionStore";
import { queryClient } from "../../../app/queryClient";
import { refreshSession } from "../../../auth/session";
import { useMeStore } from "../../../user/store/useMeStore";
import type { SseEnvelope } from "./index";

function readUserId(data: unknown): string | null {
  if (typeof data === "object" && data !== null && "user_id" in data) {
    const value = (data as { user_id: unknown }).user_id;
    return typeof value === "string" ? value : null;
  }
  return null;
}

export function handlePermissionEvent(envelope: SseEnvelope): void {
  usePermissionStore.getState().invalidate();
  void queryClient.invalidateQueries({ queryKey: ["permissions"] });

  const myId = useMeStore.getState().me?.id ?? null;
  const targetId = readUserId(envelope.data);
  const concernsMe = targetId === null || targetId === myId;

  if (concernsMe) {
    void refreshSession(true).then(() =>
      queryClient.invalidateQueries({ queryKey: ["me"] }),
    );
  }
}
