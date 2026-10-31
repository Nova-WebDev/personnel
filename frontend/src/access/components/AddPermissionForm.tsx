import { useState, type FormEvent } from "react";

import { getErrorMessage } from "../../auth/utils";
import BranchSelect from "../../organization/components/BranchSelect";
import { submitClass } from "../../organization/components/formStyles";
import { useBranches } from "../../organization/hooks/useBranches";
import UnitSelect from "../../personnel/components/UnitSelect";
import { useAddPermission } from "../hooks/usePermissionMutations";
import type { RoleInfo } from "../types";
import UserPicker from "./UserPicker";

const labelClass = "mb-1.5 block text-sm text-gray-600 dark:text-gray-300";

interface AddPermissionFormProps {
  role: RoleInfo;
  onDone: () => void;
}

export default function AddPermissionForm({
  role,
  onDone,
}: AddPermissionFormProps) {
  const { branches } = useBranches();
  const add = useAddPermission();

  const [userId, setUserId] = useState("");
  const [branchId, setBranchId] = useState("");
  const [unitId, setUnitId] = useState("");

  const units =
    branches.find((branch) => branch.branch_id === branchId)?.units ?? [];
  const canSubmit =
    userId !== "" && (!role.scoped || unitId !== "") && !add.isPending;

  const handleBranch = (id: string) => {
    setBranchId(id);
    setUnitId("");
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!canSubmit) return;
    add.mutate(
      {
        user_id: userId,
        level: role.key,
        unit_id: role.scoped ? unitId : null,
      },
      { onSuccess: onDone },
    );
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4">
      <div>
        <span className={labelClass}>کاربر</span>
        <UserPicker value={userId} onChange={setUserId} />
      </div>

      {role.scoped && (
        <>
          <div>
            <span className={labelClass}>سازمان</span>
            <BranchSelect
              branches={branches}
              value={branchId}
              onChange={handleBranch}
            />
          </div>
          <div>
            <span className={labelClass}>واحد</span>
            <UnitSelect
              units={units}
              value={unitId}
              disabled={branchId === ""}
              onChange={setUnitId}
            />
          </div>
        </>
      )}

      {add.error !== null && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(add.error, "افزودن دسترسی ناموفق بود.")}
        </p>
      )}

      <button
        type="submit"
        disabled={!canSubmit}
        className={`${submitClass} mt-6 w-full flex-none`}
      >
        {add.isPending ? "در حال ثبت..." : "ثبت"}
      </button>
    </form>
  );
}
