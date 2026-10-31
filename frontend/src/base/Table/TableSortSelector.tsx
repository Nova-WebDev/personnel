import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSort,
  faSortUp,
  faSortDown,
  faChevronDown,
} from "@fortawesome/free-solid-svg-icons";
import type { IconDefinition } from "@fortawesome/fontawesome-svg-core";
import type { TableColumn, TableSortSelectorProps } from "./types";

export default function TableSortSelector<T>({
  columns,
  orderBy,
  deorder,
  onSort,
}: TableSortSelectorProps<T>) {
  const [open, setOpen] = useState(false);

  const getIcon = (col: TableColumn<T>): IconDefinition => {
    if (!col.orderBy) return faSort;
    if (orderBy !== col.orderBy) return faSort;
    if (deorder === false) return faSortUp;
    return faSortDown;
  };

  const isActive = (col: TableColumn<T>) => orderBy === col.orderBy;

  return (
    <div className="relative ms-2 md:hidden">
      <button
        onClick={() => setOpen(!open)}
        className="px-3 py-2.5 bg-white dark:bg-[#0c242f] rounded-lg flex items-center gap-2 text-sm text-slate-800 dark:text-slate-100 border border-slate-300 dark:border-white/10"
      >
        <span>Sort</span>
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-[11px] transition-transform text-teal-600 dark:text-teal-300 ${
            open ? "rotate-180" : "rotate-0"
          }`}
        />
      </button>

      {open && (
        <div className="absolute end-0 mt-2 w-52 bg-white dark:bg-[#0c242f] border border-slate-200 dark:border-white/10 rounded-xl shadow-xl z-50 overflow-hidden">
          {columns
            .filter((c) => c.orderBy)
            .map((col, i) => (
              <button
                key={i}
                onClick={() => {
                  if (col.orderBy) onSort(col.orderBy);
                  setOpen(false);
                }}
                className={`w-full px-3 py-2.5 text-start flex items-center justify-between text-sm ${
                  isActive(col)
                    ? "bg-teal-50 dark:bg-teal-400/10 text-teal-700 dark:text-teal-300"
                    : "text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-white/5"
                }`}
              >
                <span>{col.label}</span>
                <FontAwesomeIcon icon={getIcon(col)} />
              </button>
            ))}
        </div>
      )}
    </div>
  );
}
