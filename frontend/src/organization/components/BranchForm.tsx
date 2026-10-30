import { useState, type FormEvent } from "react";

import { getErrorMessage } from "../../auth/utils";
import { useCreateBranch } from "../hooks/useCreateBranch";
import { cancelClass, fieldClass, submitClass } from "./formStyles";

interface BranchFormProps {
  onDone: () => void;
}

export default function BranchForm({ onDone }: BranchFormProps) {
  const [name, setName] = useState("");
  const create = useCreateBranch();
  const trimmed = name.trim();

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (trimmed === "" || create.isPending) return;
    create.mutate(trimmed, { onSuccess: onDone });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4">
      <div>
        <label
          htmlFor="branch-name"
          className="mb-1.5 block text-sm text-gray-600 dark:text-gray-300"
        >
          نام سازمان
        </label>
        <input
          id="branch-name"
          autoFocus
          value={name}
          onChange={(event) => setName(event.target.value)}
          maxLength={100}
          className={fieldClass}
        />
      </div>

      {create.error !== null && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(create.error, "ثبت سازمان ناموفق بود.")}
        </p>
      )}

      <div className="flex gap-3">
        <button
          type="submit"
          disabled={trimmed === "" || create.isPending}
          className={submitClass}
        >
          {create.isPending ? "در حال ثبت..." : "ثبت"}
        </button>
        <button type="button" onClick={onDone} className={cancelClass}>
          انصراف
        </button>
      </div>
    </form>
  );
}
