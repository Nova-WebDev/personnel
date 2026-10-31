import { useMutation } from "@tanstack/react-query";

import { updateBranch } from "../api";
import { useRefreshOrganization } from "./useRefreshOrganization";

export function useUpdateBranch() {
  const refresh = useRefreshOrganization();

  return useMutation({
    mutationFn: ({ id, name }: { id: string; name: string }) =>
      updateBranch(id, name),
    onSuccess: refresh,
  });
}
