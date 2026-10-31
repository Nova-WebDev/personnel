import { useMutation } from "@tanstack/react-query";

import { deleteUnit } from "../api";
import { useRefreshOrganization } from "./useRefreshOrganization";

export function useDeleteUnit() {
  const refresh = useRefreshOrganization();

  return useMutation({
    mutationFn: (id: string) => deleteUnit(id),
    onSuccess: refresh,
  });
}
