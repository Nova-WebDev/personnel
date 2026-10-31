import { useMutation } from "@tanstack/react-query";

import { deleteBranch } from "../api";
import { useRefreshOrganization } from "./useRefreshOrganization";

export function useDeleteBranch() {
  const refresh = useRefreshOrganization();

  return useMutation({
    mutationFn: (id: string) => deleteBranch(id),
    onSuccess: refresh,
  });
}
