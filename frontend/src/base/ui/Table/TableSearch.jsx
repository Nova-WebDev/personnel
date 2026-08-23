import { useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";

export default function TableSearch({ value, onChange }) {
  const timeoutRef = useRef(null);

  const handleChange = (e) => {
    const nextValue = e.target.value;

    if (timeoutRef.current) clearTimeout(timeoutRef.current);

    timeoutRef.current = setTimeout(() => {
      onChange(nextValue);
    }, 350);
  };

  return (
    <>
      <div className="mb-4 md:hidden grow">
        <div className="relative">
          <FontAwesomeIcon
            icon={faSearch}
            className="absolute text-gray-400 -translate-y-1/2 right-3 top-1/2 dark:text-gray-500"
          />
          <input
            type="text"
            defaultValue={value}
            onChange={handleChange}
            placeholder="جستجو..."
            className="
              w-full pr-10 pl-3 py-2 rounded-md text-sm
              bg-white dark:bg-[#182238]
              border border-[#D3DBEB] dark:border-[#1F2A44]
              text-gray-800 dark:text-gray-200
              placeholder-gray-400 dark:placeholder-gray-500
              focus:outline-none focus:ring-2 focus:ring-orange-500 dark:focus:ring-sky-600
              transition
            "
          />
        </div>
      </div>

      <div className="hidden mb-4 md:block grow">
        <div className="relative">
          <FontAwesomeIcon
            icon={faSearch}
            className="absolute text-gray-400 -translate-y-1/2 right-3 top-1/2 dark:text-gray-500"
          />
          <input
            type="text"
            defaultValue={value}
            onChange={handleChange}
            placeholder="جستجو..."
            className="
              w-full pr-10 pl-3 py-2 rounded-md text-sm
              bg-white dark:bg-[#182238]
              border border-[#D3DBEB] dark:border-[#1F2A44]
              text-gray-800 dark:text-gray-200
              placeholder-gray-400 dark:placeholder-gray-500
              focus:outline-none focus:ring-2 focus:ring-orange-500 dark:focus:ring-sky-600
              transition
            "
          />
        </div>
      </div>
    </>
  );
}
