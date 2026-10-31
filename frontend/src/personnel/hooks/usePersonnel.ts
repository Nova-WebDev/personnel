import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { useBranches } from "../../organization/hooks/useBranches";
import { useOrganizationStore } from "../../organization/store/useOrganizationStore";
import { isUnitAllowed } from "../../user/permissions";
import { useMeStore } from "../../user/store/useMeStore";
import { getPersonnel } from "../api";
import { usePersonnelStore } from "../store/usePersonnelStore";
import type { PersonnelView } from "../types";

export function usePersonnel() {
  const isComplete = usePersonnelStore((state) => state.isComplete);
  const users = usePersonnelStore((state) => state.users);
  const setAll = usePersonnelStore((state) => state.setAll);
  const upsertMe = usePersonnelStore((state) => state.upsertMe);
  const hrUnitIds = useMeStore((state) => state.hrUnitIds);
  const unitLookup = useOrganizationStore((state) => state.unitLookup);
  useBranches();

  const query = useQuery({
    queryKey: ["personnel"],
    queryFn: async () => (await getPersonnel()).data,
    enabled: !isComplete,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data === undefined) return;
    setAll(query.data);
    const current = useMeStore.getState().me;
    if (current !== null) upsertMe(current);
  }, [query.data, setAll, upsertMe]);

  const visible: PersonnelView[] = Object.values(users)
    .filter((user) => isUnitAllowed(hrUnitIds, user.unit_id))
    .map((user) => {
      const unit = user.unit_id === null ? undefined : unitLookup[user.unit_id];
      return {
        ...user,
        unit_name: unit?.unitName ?? null,
        branch_id: unit?.branchId ?? null,
        branch_name: unit?.branchName ?? null,
      };
    });

  console.log(
    "[usePersonnel]",
    Object.keys(users).length,
    visible.length,
    hrUnitIds,
  );

  return {
    users: visible,
    isLoading: !isComplete && query.isLoading,
    isError: query.isError,
  };
}
