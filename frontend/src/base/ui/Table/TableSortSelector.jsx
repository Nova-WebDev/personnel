import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSort,
  faSortUp,
  faSortDown,
  faChevronDown,
} from "@fortawesome/free-solid-svg-icons";

export default function TableSortSelector({ columns, orderBy, deorder, onSort }) {
  const [open, setOpen] = useState(false);

  const getIcon = (col) => {
    if (!col.orderBy) return faSort;
    if (orderBy !== col.orderBy) return faSort;
    if (deorder === false) return faSortUp;
    return faSortDown;
  };

  const isActive = (col) => orderBy === col.orderBy;

  return (
    <div className="relative mr-2 md:ml-3 md:hidden">
      <button
        onClick={() => setOpen(!open)}
        className="px-3 py-2 bg-white dark:bg-[#182238] rounded-md flex items-center gap-2 text-sm text-gray-800 dark:text-gray-100 border border-gray-300 dark:border-gray-700/40"
      >
        <span>Sort</span>
        <span className="inline-flex items-center justify-center w-5 h-5 ml-auto rounded-full">
          <FontAwesomeIcon
            icon={faChevronDown}
            className={`text-[11px] transition-transform ${
              open ? "rotate-180" : "rotate-0"
            } text-gray-500 dark:text-gray-400`}
          />
        </span>
      </button>

      {open && (
        <div className="absolute left-0 mt-2 w-52 bg-white dark:bg-[#0f1724] border border-gray-200 dark:border-gray-700 rounded-xl shadow-xl z-50 overflow-hidden">
          {columns
            .filter((c) => c.orderBy)
            .map((col, i) => (
              <button
                key={i}
                onClick={() => {
                  onSort(col.orderBy);
                  setOpen(false);
                }}
                className={`w-full px-3 py-2 text-left flex items-center justify-between text-sm ${
                  isActive(col)
                    ? "bg-blue-50 dark:bg-[#111a2b] text-blue-700 dark:text-blue-300"
                    : "text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-[#111a2b]"
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
