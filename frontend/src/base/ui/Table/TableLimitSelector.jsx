import { useState, useRef, useEffect } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown } from "@fortawesome/free-solid-svg-icons";

export default function TableLimitSelector({ limit, onChange }) {
  const [open, setOpen] = useState(false);
  const rootRef = useRef(null);
  const options = [20, 30, 50];

  useEffect(() => {
    function close(e) {
      if (!rootRef.current) return;
      if (!rootRef.current.contains(e.target)) setOpen(false);
    }
    document.addEventListener("mousedown", close);
    document.addEventListener("touchstart", close);
    return () => {
      document.removeEventListener("mousedown", close);
      document.removeEventListener("touchstart", close);
    };
  }, []);

  return (
    <div className="relative ml-2 md:ml-3" ref={rootRef}>
      <button
        onClick={() => setOpen(!open)}
        className="
          px-3 py-2 rounded-md flex items-center gap-2 text-sm
          bg-[#fbf3e9] dark:bg-[#152036]
          text-gray-800 dark:text-gray-200
          border border-gray-300 dark:border-gray-700/40
        "
      >
        <span>{limit}</span>

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
        <div
          className="
            absolute left-0 bottom-full mb-2 w-40 rounded-md shadow-xl z-50 overflow-hidden
            bg-[#fbf3e9] dark:bg-[#152036]
            border border-gray-300 dark:border-gray-700
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
                w-full px-3 py-2 text-left text-sm flex items-center justify-between
                ${
                  limit === opt
                    ? "bg-[#fcf8f0] dark:bg-gray-800 text-gray-800 dark:text-gray-200"
                    : "text-gray-600 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-[#111a2b]"
                }
              `}
            >
              <span>{opt}</span>

              {limit === opt && (
                <span className="inline-block w-2 h-2 rounded-full bg-[#f17c4a] dark:bg-[#43f9e4]" />
              )}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
