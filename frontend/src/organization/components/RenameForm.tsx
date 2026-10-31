import { useState, type FormEvent } from "react";

import { getErrorMessage } from "../../auth/utils";
import { cancelClass, fieldClass, submitClass } from "./formStyles";

interface RenameFormProps {
  label: string;
  initialName: string;
  isPending: boolean;
  error: unknown;
  onSubmit: (name: string) => void;
  onCancel: () => void;
}

export default function RenameForm({
  label,
  initialName,
  isPending,
  error,
  onSubmit,
  onCancel,
}: RenameFormProps) {
  const [name, setName] = useState(initialName);
  const trimmed = name.trim();
  const canSubmit = trimmed !== "" && trimmed !== initialName && !isPending;

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (canSubmit) onSubmit(trimmed);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4">
      <div>
        <label
          htmlFor="rename-input"
          className="mb-1.5 block text-sm text-gray-600 dark:text-gray-300"
        >
          {label}
        </label>
        <input
          id="rename-input"
          autoFocus
          value={name}
          onChange={(event) => setName(event.target.value)}
          maxLength={100}
          className={fieldClass}
        />
      </div>

      {error !== null && error !== undefined && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(error, "ویرایش ناموفق بود.")}
        </p>
      )}

      <div className="flex gap-3">
        <button type="button" onClick={onCancel} className={cancelClass}>
          انصراف
        </button>
        <button type="submit" disabled={!canSubmit} className={submitClass}>
          {isPending ? "در حال ثبت..." : "ثبت"}
        </button>
      </div>
    </form>
  );
}
