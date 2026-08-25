import { useBranchesStore } from "../../../branch/store/useBranchesStore";

export function UnitNameCell({ branchId, unitId }) {
  const branches = useBranchesStore((s) => s.branches) || [];

  if (!unitId) return "—";

  const branch = branches.find((b) => b.id === branchId);
  const unit = branch?.units?.find((u) => u.id === unitId);

  return unit ? unit.name : "—";
}