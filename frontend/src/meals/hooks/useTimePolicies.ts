import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { getTimePolicies } from "../api";
import { useTimePolicyStore } from "../store/useTimePolicyStore";

export function useTimePolicies() {
  const isComplete = useTimePolicyStore((state) => state.isComplete);
  const policies = useTimePolicyStore((state) => state.policies);
  const setPolicies = useTimePolicyStore((state) => state.setPolicies);

  const query = useQuery({
    queryKey: ["time-policies"],
    queryFn: async () => (await getTimePolicies()).data,
    enabled: !isComplete,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data !== undefined) setPolicies(query.data);
  }, [query.data, setPolicies]);

  return policies;
}
