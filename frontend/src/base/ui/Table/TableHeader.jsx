import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSort, faSortUp, faSortDown } from "@fortawesome/free-solid-svg-icons";

export default function TableHeader({ columns, orderBy, deorder, onSort }) {
  const getIcon = (col) => {
    if (!col.orderBy) return faSort;
    if (orderBy !== col.orderBy) return faSort;
    if (deorder === false) return faSortUp;
    return faSortDown;
  };

  const isActive = (col) => col.orderBy && orderBy === col.orderBy;

  return (
    <thead>
      <tr>
        {columns.map((col, i) => (
          <th
            key={i}
            onClick={() => col.orderBy && onSort(col.orderBy)}
            className={`
              px-6 py-5 font-semibold text-left whitespace-nowrap transition select-none
              ${col.orderBy ? "cursor-pointer" : ""}
              ${isActive(col) ? "text-orange-300" : "text-gray-100"}
              ${i === 0 ? "rounded-br-xl rounded-tr-xl" : ""}
              bg-[#b23d0f] dark:bg-[#002856]
            `}
          >
            <div className="flex items-center gap-2">
              <span>{col.label}</span>
              {col.orderBy && (
                <span className="inline-flex items-center justify-center w-6 h-6 rounded-full">
                  <FontAwesomeIcon
                    icon={getIcon(col)}
                    className={`text-[12px] ${
                      isActive(col) ? "text-orange-300" : "text-gray-100"
                    }`}
                  />
                </span>
              )}
            </div>
          </th>
        ))}

        <th
          className="
            px-6 py-5 font-semibold text-left text-gray-100 whitespace-nowrap
            bg-[#b23d0f] dark:bg-[#002856]
            rounded-bl-xl rounded-tl-xl
          "
        >
          Actions
        </th>
      </tr>
    </thead>
  );
}
