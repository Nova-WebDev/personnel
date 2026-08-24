import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { getAllBranches } from "../api/branchApi";
import { useBranchesStore } from "../store/useBranchesStore";

export function useGetAllBranches() {
  const { branches, isSet, setBranches } = useBranchesStore();

  const query = useQuery({
    queryKey: ["branches"],
    queryFn: getAllBranches,
    enabled: !isSet,
  });


  useEffect(() => {
    if (query.data && query.data.data && !isSet) {
      setBranches(query.data.data);
    }
  }, [query.data, isSet, setBranches]);

  return {
    branches,
    isSet,
    isLoading: !isSet && query.isLoading,
    error: query.error,
  };
}
