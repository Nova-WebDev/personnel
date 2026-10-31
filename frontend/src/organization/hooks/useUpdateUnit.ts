import { useMutation } from "@tanstack/react-query";

import { updateUnit } from "../api";
import { useRefreshOrganization } from "./useRefreshOrganization";

export function useUpdateUnit() {
  const refresh = useRefreshOrganization();

  return useMutation({
    mutationFn: ({ id, name }: { id: string; name: string }) =>
      updateUnit(id, name),
    onSuccess: refresh,
  });
}
