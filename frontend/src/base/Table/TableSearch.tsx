import { useRef } from "react";
import type { ChangeEvent } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSearch } from "@fortawesome/free-solid-svg-icons";
import type { TableSearchProps } from "./types";

export default function TableSearch({ value, onChange }: TableSearchProps) {
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const nextValue = e.target.value;

    if (timeoutRef.current) clearTimeout(timeoutRef.current);

    timeoutRef.current = setTimeout(() => {
      onChange(nextValue);
    }, 350);
  };

  return (
    <div className="mb-4 grow">
      <div className="relative">
        <FontAwesomeIcon
          icon={faSearch}
          className="absolute -translate-y-1/2 pointer-events-none start-3 top-1/2 text-teal-600 dark:text-teal-300"
        />
        <input
          type="text"
          defaultValue={value}
          onChange={handleChange}
          placeholder="جستجو..."
          className="
            w-full ps-10 pe-3 py-2.5 rounded-lg text-sm
            bg-white dark:bg-[#0c242f]
            border border-slate-300 dark:border-white/10
            text-slate-800 dark:text-slate-100
            placeholder-slate-400 dark:placeholder-slate-500
            focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20
            transition
          "
        />
      </div>
    </div>
  );
}
