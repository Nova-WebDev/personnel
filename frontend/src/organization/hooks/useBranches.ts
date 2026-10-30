import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { getBranches } from "../api";
import { useOrganizationStore } from "../store/useOrganizationStore";

export function useBranches() {
  const isComplete = useOrganizationStore((state) => state.isComplete);
  const branches = useOrganizationStore((state) => state.branches);
  const setBranches = useOrganizationStore((state) => state.setBranches);

  const query = useQuery({
    queryKey: ["branches"],
    queryFn: async () => (await getBranches()).data,
    enabled: !isComplete,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data !== undefined) setBranches(query.data);
  }, [query.data, setBranches]);

  return {
    branches,
    isLoading: !isComplete && query.isLoading,
    isError: query.isError,
    refetch: query.refetch,
  };
}
