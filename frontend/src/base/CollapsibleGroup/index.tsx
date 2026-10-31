import { faChevronDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";
import type { MouseEvent, ReactNode } from "react";

export type CollapsibleGroupVariant = "section" | "card" | "row";

export interface CollapsibleGroupAction {
  render: () => ReactNode;
}

export interface CollapsibleGroupProps {
  variant: CollapsibleGroupVariant;
  title: string;
  meta?: string;
  icon?: () => ReactNode;
  actions?: CollapsibleGroupAction[];
  defaultOpen?: boolean;
  children?: ReactNode;
}

const containerStyles: Record<CollapsibleGroupVariant, string> = {
  section:
    "w-full p-4 md:px-7 bg-teal-50 border border-teal-100 rounded-2xl dark:bg-teal-500/10 dark:border-teal-500/20",
  card: "w-full rounded-2xl border bg-white dark:bg-[#0c242f] border-slate-200 dark:border-white/10 transition-all duration-200",
  row: "w-full rounded-lg bg-slate-50 dark:bg-white/5 border border-slate-200 dark:border-white/10 text-gray-700 dark:text-gray-200",
};

const headerStyles: Record<CollapsibleGroupVariant, string> = {
  section: "flex items-center justify-between select-none",
  card: "flex items-center justify-between gap-2 p-4 select-none",
  row: "flex items-center justify-between gap-2 p-2.5",
};

const iconWrapperStyles: Record<CollapsibleGroupVariant, string> = {
  section: "",
  card: "flex items-center justify-center text-teal-600 bg-teal-50 w-9 h-9 rounded-xl dark:bg-teal-400/10 dark:text-teal-300 shrink-0",
  row: "text-xs text-teal-500 dark:text-teal-300 shrink-0",
};

const titleStyles: Record<CollapsibleGroupVariant, string> = {
  section: "text-lg font-bold text-gray-800 dark:text-gray-100",
  card: "font-semibold text-gray-800 dark:text-gray-100 truncate",
  row: "text-sm truncate",
};

export default function CollapsibleGroup({
  variant,
  title,
  meta,
  icon,
  actions,
  defaultOpen = false,
  children,
}: CollapsibleGroupProps) {
  const [open, setOpen] = useState(defaultOpen);

  const expandable = children !== undefined;
  const showDivider = Boolean(actions?.length) && expandable;

  const stop = (e: MouseEvent<HTMLElement>) => {
    e.stopPropagation();
  };

  return (
    <div className={containerStyles[variant]}>
      <div
        className={`${headerStyles[variant]} ${expandable ? "cursor-pointer" : ""}`}
        onClick={expandable ? () => setOpen(!open) : undefined}
      >
        <div className="flex items-center min-w-0 gap-3">
          {icon && <div className={iconWrapperStyles[variant]}>{icon()}</div>}
          <div className="min-w-0">
            <div className={titleStyles[variant]}>{title}</div>
            {meta && (
              <div className="text-xs text-gray-500 dark:text-gray-400">
                {meta}
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1 shrink-0">
          {actions?.map((action, i) => (
            <div key={i} onClick={stop}>
              {action.render()}
            </div>
          ))}

          {showDivider && (
            <div className="w-px h-5 mx-1 bg-slate-200 dark:bg-white/15" />
          )}

          {expandable && (
            <span className="flex h-8 w-8 items-center justify-center">
              <FontAwesomeIcon
                icon={faChevronDown}
                className={`text-gray-500 dark:text-gray-400 transition-transform duration-300 ${
                  open ? "rotate-180" : ""
                }`}
              />
            </span>
          )}
        </div>
      </div>

      {expandable && open && <div className="px-4 pb-4 pt-1">{children}</div>}
    </div>
  );
}
