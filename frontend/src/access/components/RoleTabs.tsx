import { faLock } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { ROLES, type RoleKey } from "../types";

interface RoleTabsProps {
  selected: RoleKey;
  counts: Record<RoleKey, number>;
  onSelect: (role: RoleKey) => void;
}

export default function RoleTabs({
  selected,
  counts,
  onSelect,
}: RoleTabsProps) {
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
      {ROLES.map((role) => {
        const active = role.key === selected;
        return (
          <button
            key={role.key}
            type="button"
            onClick={() => onSelect(role.key)}
            className={`flex cursor-pointer flex-col items-start gap-1 rounded-xl border p-4 text-start transition ${
              active
                ? "border-teal-600 bg-teal-600 text-white"
                : "border-slate-200 bg-white text-slate-700 hover:border-teal-400 dark:border-white/10 dark:bg-[#0c242f] dark:text-slate-200"
            }`}
          >
            <span className="flex items-center gap-2 text-sm font-semibold">
              {role.label}
              {role.locked && (
                <FontAwesomeIcon icon={faLock} className="text-xs opacity-70" />
              )}
            </span>
            <span
              className={`text-2xl font-extrabold ${active ? "text-white" : "text-teal-700 dark:text-teal-300"}`}
            >
              {counts[role.key].toLocaleString("fa-IR")}
            </span>
          </button>
        );
      })}
    </div>
  );
}
