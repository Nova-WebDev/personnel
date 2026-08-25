import { useEffect, useRef, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown } from "@fortawesome/free-solid-svg-icons";

const POSITION_OPTIONS = [
  { value: 1, label: "کارمند" },
  { value: 2, label: "کارشناس" },
  { value: 3, label: "سرپرست" },
  { value: 4, label: "مدیر" },
];

export const PositionField = ({ value, onChange }) => {
  const [open, setOpen] = useState(false);
  const containerRef = useRef(null);

  const selectedPosition = POSITION_OPTIONS.find(
    (opt) => String(opt.value) === String(value),
  );

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (positionValue) => {
    onChange(String(positionValue));
    setOpen(false);
  };

  return (
    <div ref={containerRef} className="relative">
      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="flex items-center justify-between w-full px-3 py-2 text-right border border-gray-300 dark:border-gray-600 rounded-md dark:bg-[#1C2333] dark:text-gray-100 focus:outline-none focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-1 focus:ring-indigo-400 dark:focus:ring-indigo-500 transition-colors"
      >
        <span className={selectedPosition ? "" : "text-gray-400 dark:text-gray-500"}>
          {selectedPosition ? selectedPosition.label : "انتخاب سمت (اختیاری)"}
        </span>
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-xs text-gray-400 dark:text-gray-500 transition-transform duration-200 ${
            open ? "rotate-180" : ""
          }`}
        />
      </button>

      <div
        className={`absolute z-10 w-full mt-1 overflow-hidden bg-white border border-gray-200 rounded-md shadow-lg dark:bg-[#1C2333] dark:border-gray-700 origin-top transition-all duration-150 ${
          open
            ? "opacity-100 scale-100 pointer-events-auto"
            : "opacity-0 scale-95 pointer-events-none"
        }`}
      >
        <ul className="py-1 overflow-y-auto max-h-48">
          {POSITION_OPTIONS.map((opt) => (
            <li
              key={opt.value}
              onClick={() => handleSelect(opt.value)}
              className={`px-3 py-2 text-sm cursor-pointer transition-colors ${
                String(opt.value) === String(value)
                  ? "bg-indigo-50 text-indigo-600 dark:bg-indigo-500/10 dark:text-indigo-400"
                  : "text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-[#232f52]"
              }`}
            >
              {opt.label}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};