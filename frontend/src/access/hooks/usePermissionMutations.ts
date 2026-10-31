import { useMutation, useQueryClient } from "@tanstack/react-query";

import { deleteUserPermissions, setUserPermissions } from "../api";
import { usePermissionStore } from "../store/usePermissionStore";
import type { AddPermissionInput, Permission, PermissionInput } from "../types";

function currentOf(userId: string): PermissionInput[] {
  return Object.values(usePermissionStore.getState().items)
    .filter((item) => item.user_id === userId)
    .map((item) => ({ level: item.level.toLowerCase(), scope: item.unit_id }));
}

async function save(userId: string, next: PermissionInput[]) {
  if (next.length === 0) await deleteUserPermissions(userId);
  else await setUserPermissions(userId, next);
}

function useRefresh() {
  const queryClient = useQueryClient();

  return async () => {
    usePermissionStore.getState().invalidate();
    await queryClient.invalidateQueries({ queryKey: ["permissions"] });
  };
}

export function useAddPermission() {
  const refresh = useRefresh();

  return useMutation({
    mutationFn: ({ user_id, level, unit_id }: AddPermissionInput) => {
      const wanted = level.toLowerCase();
      const current = currentOf(user_id);
      const exists = current.some(
        (item) => item.level === wanted && item.scope === unit_id,
      );
      return save(
        user_id,
        exists ? current : [...current, { level: wanted, scope: unit_id }],
      );
    },
    onSuccess: refresh,
  });
}

export function useRemovePermission() {
  const refresh = useRefresh();

  return useMutation({
    mutationFn: (permission: Permission) => {
      const level = permission.level.toLowerCase();
      const next = currentOf(permission.user_id).filter(
        (item) => !(item.level === level && item.scope === permission.unit_id),
      );
      return save(permission.user_id, next);
    },
    onSuccess: refresh,
  });
}
