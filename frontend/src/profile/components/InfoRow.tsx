import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import type { ReactNode } from "react";

interface InfoRowProps {
  icon: IconDefinition;
  label: string;
  children: ReactNode;
}

export default function InfoRow({ icon, label, children }: InfoRowProps) {
  return (
    <div className="flex items-center gap-4 py-3.5">
      <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-teal-500/10 text-teal-600 dark:bg-teal-400/10 dark:text-teal-300">
        <FontAwesomeIcon icon={icon} />
      </span>
      <div className="min-w-0 flex-1">
        <p className="text-xs text-slate-500 dark:text-slate-400">{label}</p>
        <div className="mt-0.5 truncate font-medium text-slate-900 dark:text-slate-100">
          {children}
        </div>
      </div>
    </div>
  );
}
