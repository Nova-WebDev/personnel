import { useState, type FormEvent } from "react";

import { getErrorMessage } from "../../auth/utils";
import { useCreateUnit } from "../hooks/useCreateUnit";
import type { Branch } from "../types";
import BranchSelect from "./BranchSelect";
import { cancelClass, fieldClass, submitClass } from "./formStyles";

interface UnitFormProps {
  branches: Branch[];
  onDone: () => void;
}

export default function UnitForm({ branches, onDone }: UnitFormProps) {
  const [name, setName] = useState("");
  const [branchId, setBranchId] = useState("");
  const create = useCreateUnit();
  const trimmed = name.trim();
  const canSubmit = trimmed !== "" && branchId !== "" && !create.isPending;

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!canSubmit) return;
    create.mutate({ name: trimmed, branchId }, { onSuccess: onDone });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4">
      <div>
        <span className="mb-1.5 block text-sm text-gray-600 dark:text-gray-300">
          سازمان
        </span>
        <BranchSelect
          branches={branches}
          value={branchId}
          onChange={setBranchId}
        />
      </div>

      <div>
        <label
          htmlFor="unit-name"
          className="mb-1.5 block text-sm text-gray-600 dark:text-gray-300"
        >
          نام واحد
        </label>
        <input
          id="unit-name"
          value={name}
          onChange={(event) => setName(event.target.value)}
          maxLength={100}
          className={fieldClass}
        />
      </div>

      {create.error !== null && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(create.error, "ثبت واحد ناموفق بود.")}
        </p>
      )}

      <div className="flex gap-3">
        <button type="submit" disabled={!canSubmit} className={submitClass}>
          {create.isPending ? "در حال ثبت..." : "ثبت"}
        </button>
        <button type="button" onClick={onDone} className={cancelClass}>
          انصراف
        </button>
      </div>
    </form>
  );
}
