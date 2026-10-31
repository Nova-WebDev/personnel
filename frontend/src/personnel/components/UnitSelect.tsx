import { faCheck, faChevronDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useEffect, useRef, useState } from "react";

import { fieldClass } from "../../organization/components/formStyles";
import type { Unit } from "../../organization/types";

interface UnitSelectProps {
  units: Unit[];
  value: string;
  disabled: boolean;
  onChange: (unitId: string) => void;
}

export default function UnitSelect({
  units,
  value,
  disabled,
  onChange,
}: UnitSelectProps) {
  const [open, setOpen] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  const selected = units.find((unit) => unit.unit_id === value);

  useEffect(() => {
    const close = (event: MouseEvent) => {
      if (ref.current !== null && !ref.current.contains(event.target as Node))
        setOpen(false);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        type="button"
        disabled={disabled}
        onClick={() => setOpen((state) => !state)}
        aria-expanded={open}
        className={`${fieldClass} flex cursor-pointer items-center justify-between text-start disabled:cursor-not-allowed disabled:opacity-60`}
      >
        <span
          className={
            selected === undefined ? "text-gray-400 dark:text-gray-500" : ""
          }
        >
          {selected?.unit_name ?? "انتخاب واحد"}
        </span>
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-xs text-gray-400 transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      {open && (
        <ul className="absolute inset-x-0 top-full z-10 mt-1 max-h-56 overflow-y-auto rounded-lg border border-gray-200 bg-white p-1 shadow-lg dark:border-gray-700 dark:bg-[#0f1a2e]">
          {units.length === 0 && (
            <li className="px-3 py-2 text-sm text-gray-500">
              واحدی وجود ندارد.
            </li>
          )}
          {units.map((unit) => {
            const isSelected = unit.unit_id === value;
            return (
              <li key={unit.unit_id}>
                <button
                  type="button"
                  onClick={() => {
                    onChange(unit.unit_id);
                    setOpen(false);
                  }}
                  className={`flex w-full cursor-pointer items-center justify-between rounded-md px-3 py-2 text-sm transition ${
                    isSelected
                      ? "bg-teal-500/10 font-medium text-teal-700 dark:text-teal-300"
                      : "text-gray-700 hover:bg-gray-100 dark:text-gray-200 dark:hover:bg-white/5"
                  }`}
                >
                  {unit.unit_name}
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
