import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { getPermissions } from "../api";
import { usePermissionStore } from "../store/usePermissionStore";

export function usePermissions() {
  const isComplete = usePermissionStore((state) => state.isComplete);
  const items = usePermissionStore((state) => state.items);
  const setAll = usePermissionStore((state) => state.setAll);

  const query = useQuery({
    queryKey: ["permissions"],
    queryFn: async () => (await getPermissions()).data,
    enabled: !isComplete,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data !== undefined) setAll(query.data);
  }, [query.data, setAll]);

  return {
    permissions: Object.values(items),
    isLoading: !isComplete && query.isLoading,
    isError: query.isError,
  };
}
