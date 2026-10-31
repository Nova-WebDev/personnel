import type { Scope } from "../../user/types";

const LABELS: Record<string, string> = {
  admin: "ادمین",
  kitchen: "آشپز",
  group_manager: "مدیر گروه",
  hr_manager: "منابع انسانی",
};

export default function RoleBadges({ scopes }: { scopes: Scope[] }) {
  if (scopes.length === 0) {
    return (
      <p className="text-sm text-slate-500 dark:text-slate-400">
        دسترسی ویژه‌ای ندارید.
      </p>
    );
  }

  return (
    <ul className="flex flex-wrap gap-2">
      {scopes.map((scope, index) => {
        const level = scope.level.toLowerCase();
        const place = [scope.unit_name, scope.branch_name]
          .filter(Boolean)
          .join(" · ");

        return (
          <li
            key={`${level}-${scope.unit_id ?? "all"}-${index}`}
            className="rounded-xl border border-teal-500/30 bg-teal-500/10 px-3 py-2 text-sm text-teal-800 dark:text-teal-200"
          >
            <span className="font-semibold">{LABELS[level] ?? level}</span>
            {place !== "" && (
              <span className="ms-2 text-xs opacity-80">{place}</span>
            )}
          </li>
        );
      })}
    </ul>
  );
}
