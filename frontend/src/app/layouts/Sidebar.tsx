import { faRightFromBracket } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { NavLink } from "react-router-dom";

import { useLogout } from "../../auth/hooks/useLogout";
import Avatar from "../../shared/ui/Avatar";
import ThemeToggle from "../../shared/ui/ThemeToggle";
import { hasAnyLevel } from "../../user/permissions";
import type { Me } from "../../user/types";
import { menuGroups } from "../navigation/menu";

interface SidebarProps {
  me: Me;
  onNavigate: () => void;
}

export default function Sidebar({ me, onNavigate }: SidebarProps) {
  const logout = useLogout();

  const groups = menuGroups
    .map((group) => ({
      ...group,
      items: group.items.filter((item) => hasAnyLevel(me, item.levels)),
    }))
    .filter((group) => group.items.length > 0);

  const fullName = `${me.first_name} ${me.last_name}`.trim() || "کاربر";
  const place = [me.unit_name, me.branch_name].filter(Boolean).join(" · ");

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center gap-3 border-b border-slate-200 p-4 dark:border-white/10">
        <Avatar
          id={me.id}
          photoPath={me.photo_path}
          className="h-12 w-12 shrink-0"
        />
        <div className="min-w-0 flex-1">
          <p className="truncate font-semibold text-slate-900 dark:text-slate-100">
            {fullName}
          </p>
          <p className="truncate text-xs text-slate-500 dark:text-slate-400">
            {place || "بدون واحد"}
          </p>
        </div>
        <ThemeToggle />
      </div>

      <nav className="flex-1 space-y-5 overflow-y-auto p-3">
        {groups.map((group) => (
          <div key={group.label}>
            <p className="mb-1 px-3 text-xs font-medium text-slate-400 dark:text-slate-500">
              {group.label}
            </p>
            <ul className="space-y-1">
              {group.items.map((item) => (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    onClick={onNavigate}
                    className={({ isActive }) =>
                      `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                        isActive
                          ? "bg-teal-500/10 text-teal-700 dark:bg-teal-400/10 dark:text-teal-300"
                          : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-white/5"
                      }`
                    }
                  >
                    <FontAwesomeIcon icon={item.icon} className="w-4" />
                    {item.label}
                  </NavLink>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </nav>

      <div className="border-t border-slate-200 p-3 dark:border-white/10">
        <button
          type="button"
          onClick={() => logout.mutate()}
          disabled={logout.isPending}
          className="flex w-full cursor-pointer items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-red-600 transition hover:bg-red-50 disabled:opacity-60 dark:text-red-400 dark:hover:bg-red-500/10"
        >
          <FontAwesomeIcon icon={faRightFromBracket} className="w-4" />
          خروج
        </button>
      </div>
    </div>
  );
}
