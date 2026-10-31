import { useBranches } from "../../organization/hooks/useBranches";
import { useMeStore } from "../../user/store/useMeStore";

export function useAllowedBranches() {
  const { branches, ...rest } = useBranches();
  const hrUnitIds = useMeStore((state) => state.hrUnitIds);

  const filtered =
    hrUnitIds === null
      ? branches
      : branches
          .map((branch) => ({
            ...branch,
            units: branch.units.filter((unit) => hrUnitIds.has(unit.unit_id)),
          }))
          .filter((branch) => branch.units.length > 0);

  return { branches: filtered, ...rest };
}
