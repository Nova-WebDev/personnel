import { formatDay, formatShort } from "../../meals/utils/dates";

interface DayPickerProps {
  days: string[];
  selected: string;
  reservedDays: Set<string>;
  today: string;
  onSelect: (day: string) => void;
}

export default function DayPicker({
  days,
  selected,
  reservedDays,
  today,
  onSelect,
}: DayPickerProps) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-1 lg:overflow-visible">
      {days.map((day) => {
        const isSelected = day === selected;
        return (
          <button
            key={day}
            type="button"
            onClick={() => onSelect(day)}
            className={`relative flex min-w-[84px] shrink-0 cursor-pointer flex-col items-center gap-0.5 rounded-xl border px-3 py-3 transition lg:min-w-0 lg:flex-1 lg:py-4 ${
              isSelected
                ? "border-teal-600 bg-teal-600 text-white"
                : "border-slate-200 bg-white text-slate-700 hover:border-teal-400 dark:border-white/10 dark:bg-[#0c242f] dark:text-slate-200"
            }`}
          >
            <span className="text-xs opacity-80">
              {day === today ? "امروز" : formatDay(day)}
            </span>
            <span className="text-sm font-bold">{formatShort(day)}</span>
            {reservedDays.has(day) && (
              <span
                className={`absolute end-2 top-2 h-2 w-2 rounded-full ${isSelected ? "bg-white" : "bg-teal-500"}`}
              />
            )}
          </button>
        );
      })}
    </div>
  );
}
