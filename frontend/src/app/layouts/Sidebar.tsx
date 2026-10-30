import {
  faChevronDown,
  faRightFromBracket,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";
import { NavLink, useLocation } from "react-router-dom";

import { useLogout } from "../../auth/hooks/useLogout";
import { confirmLogout } from "../../shared/ui/confirmLogout";
import { hasAnyLevel } from "../../user/permissions";
import type { Me } from "../../user/types";
import { menuGroups, topItems, type MenuItem } from "../navigation/menu";
import { useTheme } from "../providers/useTheme";

interface SidebarProps {
  me: Me;
  onNavigate: () => void;
}

function ItemLink({
  item,
  onNavigate,
  nested = false,
}: {
  item: MenuItem;
  onNavigate: () => void;
  nested?: boolean;
}) {
  return (
    <NavLink
      to={item.to}
      end={item.to === "/"}
      onClick={onNavigate}
      className={({ isActive }) =>
        `group relative flex items-center gap-3 rounded-xl px-3 text-[15px] font-medium transition ${
          nested ? "h-10" : "h-12"
        } ${
          isActive
            ? "bg-teal-500/10 text-teal-700 dark:bg-teal-400/10 dark:text-teal-300"
            : "text-slate-600 hover:bg-slate-900/5 dark:text-slate-300 dark:hover:bg-white/5"
        }`
      }
    >
      {({ isActive }) => (
        <>
          {isActive && (
            <span className="absolute -right-3 bottom-2.5 top-2.5 w-1 rounded-full bg-linear-to-b from-teal-400 to-cyan-400 shadow-[0_0_12px_rgba(45,212,191,0.8)]" />
          )}
          {!nested && (
            <span
              className={`flex h-9 w-9 items-center justify-center rounded-lg transition ${
                isActive
                  ? "bg-linear-to-br from-teal-500 to-cyan-500 text-white shadow-md shadow-teal-500/30"
                  : "bg-slate-100 text-slate-500 group-hover:text-teal-600 dark:bg-white/5 dark:text-slate-400"
              }`}
            >
              <FontAwesomeIcon icon={item.icon} />
            </span>
          )}
          {nested && (
            <FontAwesomeIcon
              icon={item.icon}
              className="w-4 text-[13px] opacity-70"
            />
          )}
          {item.label}
        </>
      )}
    </NavLink>
  );
}

export default function Sidebar({ me, onNavigate }: SidebarProps) {
  const logout = useLogout();
  const { theme } = useTheme();
  const { pathname } = useLocation();

  const groups = menuGroups
    .map((group) => ({
      ...group,
      items: group.items.filter((item) => hasAnyLevel(me, item.levels)),
    }))
    .filter((group) => group.items.length > 0);

  const [openGroups, setOpenGroups] = useState<Record<string, boolean>>(() =>
    Object.fromEntries(
      groups.map((group) => [
        group.id,
        group.items.some((item) => pathname.startsWith(item.to)),
      ]),
    ),
  );

  const toggle = (id: string) =>
    setOpenGroups((state) => ({ ...state, [id]: !state[id] }));

  const handleLogout = async () => {
    if (await confirmLogout(theme === "dark")) {
      onNavigate();
      logout.mutate();
    }
  };

  const reports = groups.find((group) => group.id === "reports");
  const others = groups.filter((group) => group.id !== "reports");
  const ordered = reports ? [reports, ...others] : others;

  return (
    <div className="flex h-full flex-col">
      <nav className="flex-1 space-y-1.5 overflow-y-auto p-3">
        {ordered.map((group) => {
          const isOpen = openGroups[group.id] ?? false;
          return (
            <div key={group.id}>
              <button
                type="button"
                onClick={() => toggle(group.id)}
                aria-expanded={isOpen}
                className="flex h-12 w-full cursor-pointer items-center gap-3 rounded-xl px-3 text-[15px] font-semibold text-slate-800 transition hover:bg-slate-900/5 dark:text-slate-100 dark:hover:bg-white/5"
              >
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-slate-100 text-slate-500 dark:bg-white/5 dark:text-slate-400">
                  <FontAwesomeIcon icon={group.icon} />
                </span>
                <span className="flex-1 text-start">{group.label}</span>
                <FontAwesomeIcon
                  icon={faChevronDown}
                  className={`text-xs text-slate-400 transition-transform ${isOpen ? "rotate-180" : ""}`}
                />
              </button>

              {isOpen && (
                <ul className="mt-1 space-y-1">
                  {group.items.map((item) => (
                    <li key={item.to}>
                      <ItemLink item={item} onNavigate={onNavigate} nested />
                    </li>
                  ))}
                </ul>
              )}
            </div>
          );
        })}

        <div className="my-2 border-t border-slate-200 dark:border-white/10" />

        {topItems.map((item) => (
          <ItemLink key={item.to} item={item} onNavigate={onNavigate} />
        ))}
      </nav>

      <div className="border-t border-slate-200 p-3 dark:border-white/10">
        <button
          type="button"
          onClick={() => void handleLogout()}
          disabled={logout.isPending}
          className="flex h-12 w-full cursor-pointer items-center gap-3 rounded-xl px-3 text-[15px] font-medium text-red-600 transition hover:bg-red-50 disabled:opacity-60 dark:text-red-400 dark:hover:bg-red-500/10"
        >
          <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-red-50 dark:bg-red-500/10">
            <FontAwesomeIcon icon={faRightFromBracket} />
          </span>
          خروج از حساب
        </button>
      </div>
    </div>
  );
}
