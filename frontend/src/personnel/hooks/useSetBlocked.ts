import { useMutation } from "@tanstack/react-query";

import { setBlocked } from "../api";
import { usePersonnelStore } from "../store/usePersonnelStore";

export function useSetBlocked() {
  return useMutation({
    mutationFn: ({ id, isBlocked }: { id: string; isBlocked: boolean }) =>
      setBlocked(id, isBlocked),
    onSuccess: (_data, { id, isBlocked }) => {
      const { users, upsert } = usePersonnelStore.getState();
      const user = users[id];
      if (user !== undefined) upsert({ ...user, is_blocked: isBlocked });
    },
  });
}
