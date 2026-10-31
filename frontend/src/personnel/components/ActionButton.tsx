import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ReactNode } from "react";

type Tone = "neutral" | "danger" | "success";

interface ActionButtonProps {
  tone?: Tone;
  icon?: IconDefinition;
  disabled?: boolean;
  title?: string;
  onClick: () => void;
  children: ReactNode;
}

const toneClass: Record<Tone, string> = {
  neutral:
    "border-slate-300 text-slate-700 hover:bg-slate-100 dark:border-white/15 dark:text-slate-200 dark:hover:bg-white/10",
  danger:
    "border-red-300 text-red-600 hover:bg-red-50 dark:border-red-400/40 dark:text-red-400 dark:hover:bg-red-500/10",
  success:
    "border-emerald-300 text-emerald-600 hover:bg-emerald-50 dark:border-emerald-400/40 dark:text-emerald-400 dark:hover:bg-emerald-500/10",
};

export default function ActionButton({
  tone = "neutral",
  icon,
  disabled = false,
  title,
  onClick,
  children,
}: ActionButtonProps) {
  return (
    <button
      type="button"
      dir="ltr"
      disabled={disabled}
      title={title}
      onClick={onClick}
      className={`flex h-9 w-full min-w-24 items-center justify-center gap-2 rounded-lg border px-3 text-center text-xs font-medium leading-none whitespace-nowrap transition md:w-auto ${toneClass[tone]} ${
        disabled
          ? "cursor-not-allowed opacity-40 hover:bg-transparent dark:hover:bg-transparent"
          : "cursor-pointer"
      }`}
    >
      {icon !== undefined && <FontAwesomeIcon icon={icon} />}
      {children}
    </button>
  );
}
