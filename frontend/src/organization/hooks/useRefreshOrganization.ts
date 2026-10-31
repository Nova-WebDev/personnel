import { useQueryClient } from "@tanstack/react-query";

import { useOrganizationStore } from "../store/useOrganizationStore";

export function useRefreshOrganization() {
  const queryClient = useQueryClient();
  const invalidate = useOrganizationStore((state) => state.invalidate);

  return async () => {
    invalidate();
    await queryClient.invalidateQueries({ queryKey: ["branches"] });
  };
}
