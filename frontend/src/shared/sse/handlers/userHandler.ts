import { endSession } from "../../../auth/session";
import { queryClient } from "../../../app/queryClient";
import { usePersonnelStore } from "../../../personnel/store/usePersonnelStore";
import type { Personnel } from "../../../personnel/types";
import { useMeStore } from "../../../user/store/useMeStore";
import type { SseEnvelope } from "./index";

function isPersonnel(value: unknown): value is Personnel {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "first_name" in value &&
    "last_name" in value &&
    "phone" in value
  );
}

function readId(data: unknown): string | null {
  if (typeof data === "object" && data !== null && "id" in data) {
    const id = (data as { id: unknown }).id;
    return typeof id === "string" ? id : null;
  }
  return null;
}

function readBlocked(data: unknown): boolean | undefined {
  if (typeof data === "object" && data !== null && "is_blocked" in data) {
    const value = (data as { is_blocked: unknown }).is_blocked;
    return typeof value === "boolean" ? value : undefined;
  }
  return undefined;
}

function refetchPersonnel(): void {
  usePersonnelStore.getState().invalidate();
  void queryClient.invalidateQueries({ queryKey: ["personnel"] });
}

export function handleUserEvent(envelope: SseEnvelope): void {
  const store = usePersonnelStore.getState();
  const { event, data } = envelope;
  const myId = useMeStore.getState().me?.id ?? null;

  console.log("[user handler]", event, isPersonnel(data), store.isComplete);

  if (event === "user.created" || event === "user.updated") {
    if (isPersonnel(data)) {
      store.upsert(data);
      console.log(
        "[user handler] upserted",
        Object.keys(usePersonnelStore.getState().users).length,
      );
    } else refetchPersonnel();
  } else if (event === "user.blocked_status_changed") {
    const id = readId(data);
    const isBlocked = readBlocked(data);

    if (id !== null && id === myId && isBlocked === true) {
      endSession();
      return;
    }

    const user = id === null ? undefined : store.users[id];
    if (user !== undefined && isBlocked !== undefined)
      store.upsert({ ...user, is_blocked: isBlocked });
    else refetchPersonnel();
  } else if (event === "user.deleted") {
    const id = readId(data);
    if (id !== null && id === myId) {
      endSession();
      return;
    }
    if (id !== null) store.remove(id);
    else refetchPersonnel();
  } else if (event.startsWith("user.")) {
    refetchPersonnel();
  }

  void queryClient.invalidateQueries({ queryKey: ["me"] });
}
