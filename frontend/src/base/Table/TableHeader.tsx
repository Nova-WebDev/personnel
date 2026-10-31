import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faSort,
  faSortUp,
  faSortDown,
} from "@fortawesome/free-solid-svg-icons";
import type { IconDefinition } from "@fortawesome/fontawesome-svg-core";
import type { TableColumn, TableHeaderProps } from "./types";

export default function TableHeader<T>({
  columns,
  orderBy,
  deorder,
  onSort,
}: TableHeaderProps<T>) {
  const getIcon = (col: TableColumn<T>): IconDefinition => {
    if (!col.orderBy) return faSort;
    if (orderBy !== col.orderBy) return faSort;
    if (deorder === false) return faSortUp;
    return faSortDown;
  };

  const isActive = (col: TableColumn<T>) =>
    Boolean(col.orderBy) && orderBy === col.orderBy;

  return (
    <thead>
      <tr>
        {columns.map((col, i) => (
          <th
            key={i}
            onClick={() => col.orderBy && onSort(col.orderBy)}
            className={`
              px-6 py-5 font-semibold text-center whitespace-nowrap transition select-none
              ${col.orderBy ? "cursor-pointer hover:bg-teal-700 dark:hover:bg-[#12384a]" : ""}
              ${isActive(col) ? "text-white" : "text-teal-50"}
              ${i === 0 ? "rounded-s-xl" : ""}
              bg-teal-600 dark:bg-[#0f3140]
            `}
          >
            <div className="flex items-center justify-center gap-2">
              <span>{col.label}</span>
              {col.orderBy && (
                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full">
                  <FontAwesomeIcon
                    icon={getIcon(col)}
                    className={`text-[12px] ${isActive(col) ? "text-white" : "text-teal-100/70"}`}
                  />
                </span>
              )}
            </div>
          </th>
        ))}

        <th
          className="
            px-6 py-5 font-semibold text-center text-teal-50 whitespace-nowrap
            bg-teal-600 dark:bg-[#0f3140]
            rounded-e-xl
          "
        >
          Actions
        </th>
      </tr>
    </thead>
  );
}
