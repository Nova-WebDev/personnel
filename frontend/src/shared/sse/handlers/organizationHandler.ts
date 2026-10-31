import { queryClient } from "../../../app/queryClient";
import { useOrganizationStore } from "../../../organization/store/useOrganizationStore";
import { usePersonnelStore } from "../../../personnel/store/usePersonnelStore";
import type { SseEnvelope } from "./index";

function readString(data: unknown, key: string): string | null {
  if (typeof data === "object" && data !== null && key in data) {
    const value = (data as Record<string, unknown>)[key];
    return typeof value === "string" ? value : null;
  }
  return null;
}

function refetch(): void {
  useOrganizationStore.getState().invalidate();
  void queryClient.invalidateQueries({ queryKey: ["branches"] });
}

export function handleOrganizationEvent(envelope: SseEnvelope): void {
  const store = useOrganizationStore.getState();
  const { event, data } = envelope;
  const id = readString(data, "id");
  const name = readString(data, "name");

  if (event === "branch.created" && id !== null && name !== null) {
    store.addBranch(id, name);
  } else if (event === "unit.created" && id !== null && name !== null) {
    const branchId = readString(data, "branch_id");
    if (branchId === null) refetch();
    else store.addUnit(id, name, branchId);
  } else {
    refetch();
    if (event.endsWith(".deleted")) {
      usePersonnelStore.getState().invalidate();
      void queryClient.invalidateQueries({ queryKey: ["personnel"] });
    }
  }

  void queryClient.invalidateQueries({ queryKey: ["me"] });
}
