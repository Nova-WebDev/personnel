import { useBranchesStore } from "../../../branch/store/useBranchesStore";

export function BranchNameCell({ branchId }) {
  const branches = useBranchesStore((s) => s.branches) || [];
  const branch = branches.find((b) => b.id === branchId);
  return branch ? branch.name : "—";
}