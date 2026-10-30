import { faBars } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import Avatar from "../../shared/ui/Avatar";
import ThemeToggle from "../../shared/ui/ThemeToggle";
import type { Me } from "../../user/types";

interface HeaderProps {
  me: Me;
  onMenu: () => void;
}

export default function Header({ me, onMenu }: HeaderProps) {
  const fullName = `${me.first_name} ${me.last_name}`.trim() || "کاربر";

  return (
    <header
      dir="ltr"
      className="fixed inset-x-3 top-3 z-40 flex h-16 items-center gap-3 rounded-2xl border border-slate-300 bg-white px-4 shadow-[0_2px_8px_rgba(15,23,42,0.08)] dark:border-white/10 dark:bg-[#0c242f] dark:shadow-none"
    >
      <span className="hidden text-[15px] font-bold text-slate-900 sm:block dark:text-slate-100">
        {fullName}
      </span>
      <Avatar id={me.id} photoPath={me.photo_path} className="h-11 w-11" />
      <ThemeToggle />

      <div className="flex-1" />

      <span className="hidden text-xl font-black tracking-tight text-teal-700 lg:block dark:text-teal-300">
        Hooman Holding
      </span>

      <button
        type="button"
        onClick={onMenu}
        aria-label="باز کردن منو"
        className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-xl text-lg text-slate-700 hover:bg-slate-900/5 lg:hidden dark:text-slate-200 dark:hover:bg-white/10"
      >
        <FontAwesomeIcon icon={faBars} />
      </button>
    </header>
  );
}
