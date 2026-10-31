import { useState } from "react";

import { fieldClass } from "../../organization/components/formStyles";
import { usePersonnelStore } from "../../personnel/store/usePersonnelStore";
import Avatar from "../../shared/ui/Avatar";

interface UserPickerProps {
  value: string;
  onChange: (userId: string) => void;
}

export default function UserPicker({ value, onChange }: UserPickerProps) {
  const users = usePersonnelStore((state) => state.users);
  const [query, setQuery] = useState("");

  const selected = value === "" ? undefined : users[value];
  const needle = query.trim().toLowerCase();
  const matches =
    needle === ""
      ? []
      : Object.values(users)
          .filter((user) =>
            `${user.first_name} ${user.last_name} ${user.phone} ${user.personnel_code ?? ""}`
              .toLowerCase()
              .includes(needle),
          )
          .slice(0, 6);

  if (selected !== undefined) {
    return (
      <div className="flex items-center gap-3 rounded-lg border border-teal-500 bg-teal-50 p-2.5 dark:bg-teal-400/10">
        <Avatar
          id={selected.id}
          photoPath={selected.photo_path}
          className="h-9 w-9"
        />
        <span className="flex-1 font-medium text-slate-900 dark:text-slate-100">
          {selected.first_name} {selected.last_name}
        </span>
        <button
          type="button"
          onClick={() => onChange("")}
          className="cursor-pointer text-xs text-slate-500 hover:text-red-600 dark:text-slate-400"
        >
          تغییر
        </button>
      </div>
    );
  }

  return (
    <div>
      <input
        value={query}
        onChange={(event) => setQuery(event.target.value)}
        placeholder="جستجوی نام، موبایل یا کد پرسنلی"
        className={fieldClass}
      />
      {matches.length > 0 && (
        <ul className="mt-2 space-y-1 rounded-lg border border-slate-200 bg-white p-1 dark:border-white/10 dark:bg-[#0f1a2e]">
          {matches.map((user) => (
            <li key={user.id}>
              <button
                type="button"
                onClick={() => onChange(user.id)}
                className="flex w-full cursor-pointer items-center gap-3 rounded-md p-2 text-start transition hover:bg-slate-100 dark:hover:bg-white/5"
              >
                <Avatar
                  id={user.id}
                  photoPath={user.photo_path}
                  className="h-8 w-8"
                />
                <span className="text-sm text-slate-800 dark:text-slate-100">
                  {user.first_name} {user.last_name}
                </span>
                <span dir="ltr" className="ms-auto text-xs text-slate-400">
                  {user.phone}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
