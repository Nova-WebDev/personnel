import { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown } from "@fortawesome/free-solid-svg-icons";
import type { TableLimitSelectorProps } from "./types";

const options = [20, 30, 50] as const;

export default function TableLimitSelector({
  limit,
  onChange,
}: TableLimitSelectorProps) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function close(e: MouseEvent | TouchEvent) {
      if (!rootRef.current) return;
      if (!rootRef.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", close);
    document.addEventListener("touchstart", close);
    return () => {
      document.removeEventListener("mousedown", close);
      document.removeEventListener("touchstart", close);
    };
  }, []);

  return (
    <div className="relative ms-2 md:ms-3" ref={rootRef}>
      <button
        onClick={() => setOpen(!open)}
        className="
          px-3 py-2 rounded-lg flex items-center gap-2 text-sm
          bg-white dark:bg-[#0c242f]
          text-slate-800 dark:text-slate-100
          border border-slate-300 dark:border-white/10
        "
      >
        <span>{limit}</span>
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-[11px] transition-transform text-teal-600 dark:text-teal-300 ${
            open ? "rotate-180" : "rotate-0"
          }`}
        />
      </button>

      {open && (
        <div
          className="
            absolute end-0 bottom-full mb-2 w-32 rounded-lg shadow-xl z-50 overflow-hidden
            bg-white dark:bg-[#0c242f]
            border border-slate-200 dark:border-white/10
          "
        >
          {options.map((opt) => (
            <button
              key={opt}
              onClick={() => {
                onChange(opt);
                setOpen(false);
              }}
              className={`
                w-full px-3 py-2 text-start text-sm flex items-center justify-between
                ${
                  limit === opt
                    ? "bg-teal-50 dark:bg-teal-400/10 text-teal-700 dark:text-teal-300"
                    : "text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-white/5"
                }
              `}
            >
              <span>{opt}</span>

              {limit === opt && (
                <span className="inline-block w-2 h-2 rounded-full bg-teal-500 dark:bg-teal-300" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
