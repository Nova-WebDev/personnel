import { faMoon, faSun } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { useTheme } from "../../app/providers/useTheme";

export default function ThemeToggle() {
  const { theme, changeTheme } = useTheme();
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      onClick={() => changeTheme(isDark ? "light" : "dark")}
      aria-label={isDark ? "حالت روشن" : "حالت تیره"}
      className="flex h-9 w-9 cursor-pointer items-center justify-center rounded-lg text-slate-500 transition hover:bg-slate-100 hover:text-teal-600 dark:text-slate-400 dark:hover:bg-white/10 dark:hover:text-teal-300"
    >
      <FontAwesomeIcon icon={isDark ? faSun : faMoon} />
    </button>
  );
}
