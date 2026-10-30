import { faCheck, faChevronDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useEffect, useRef, useState, type KeyboardEvent } from "react";

import type { Branch } from "../types";
import { fieldClass } from "./formStyles";

interface BranchSelectProps {
  branches: Branch[];
  value: string;
  onChange: (branchId: string) => void;
}

export default function BranchSelect({
  branches,
  value,
  onChange,
}: BranchSelectProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const selected = branches.find((branch) => branch.branch_id === value);

  useEffect(() => {
    const close = (event: MouseEvent) => {
      if (ref.current !== null && !ref.current.contains(event.target as Node))
        setOpen(false);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  const handleKeyDown = (event: KeyboardEvent<HTMLButtonElement>) => {
    if (event.key === "Escape") setOpen(false);
  };

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        onClick={() => setOpen((state) => !state)}
        onKeyDown={handleKeyDown}
        aria-haspopup="listbox"
        aria-expanded={open}
        className={`${fieldClass} flex cursor-pointer items-center justify-between text-start`}
      >
        <span
          className={
            selected === undefined ? "text-gray-400 dark:text-gray-500" : ""
          }
        >
          {selected?.branch_name ?? "انتخاب سازمان"}
        </span>
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-xs text-gray-400 transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open && (
        <ul
          role="listbox"
          className="absolute inset-x-0 top-full z-10 mt-1 max-h-56 overflow-y-auto rounded-lg border border-gray-200 bg-white p-1 shadow-lg dark:border-gray-700 dark:bg-[#0f1a2e]"
        >
          {branches.length === 0 && (
            <li className="px-3 py-2 text-sm text-gray-500">
              سازمانی وجود ندارد.
            </li>
          )}
          {branches.map((branch) => {
            const isSelected = branch.branch_id === value;
            return (
              <li
                key={branch.branch_id}
                role="option"
                aria-selected={isSelected}
              >
                <button
                  type="button"
                  onClick={() => {
                    onChange(branch.branch_id);
                    setOpen(false);
                  }}
                  className={`flex w-full cursor-pointer items-center justify-between rounded-md px-3 py-2 text-sm transition ${
                    isSelected
                      ? "bg-teal-500/10 font-medium text-teal-700 dark:text-teal-300"
                      : "text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-white/5"
                  }`}
                >
                  {branch.branch_name}
                  {isSelected && (
                    <FontAwesomeIcon icon={faCheck} className="text-xs" />
                  )}
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
