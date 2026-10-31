import { useRef } from "react";

import {
  MAX_DAYS_BEFORE,
  fromTimeValue,
  toTimeValue,
  type Deadline,
  type WeekdayInfo,
} from "../utils/cutoff";

interface PolicyRowProps {
  day: WeekdayInfo;
  value: Deadline;
  onChange: (value: Deadline) => void;
}

const DAY_OPTIONS = Array.from(
  { length: MAX_DAYS_BEFORE },
  (_, index) => index + 1,
);
const DAY_NAMES = [
  "یکشنبه",
  "دوشنبه",
  "سه‌شنبه",
  "چهارشنبه",
  "پنجشنبه",
  "جمعه",
  "شنبه",
];
const ARROW =
  "bg-[url('data:image/svg+xml;utf8,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 20 20%22 fill=%22%2394a3b8%22><path d=%22M5.5 7.5 10 12l4.5-4.5%22 stroke=%22%2394a3b8%22 stroke-width=%222%22 fill=%22none%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22/></svg>')] bg-[length:1.1rem] bg-[position:left_0.75rem_center] bg-no-repeat";
const controlClass =
  "h-11 w-full cursor-pointer rounded-lg border border-slate-300 bg-white px-3 text-sm text-slate-900 transition focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-500/20 dark:border-white/10 dark:bg-[#0a1220] dark:text-slate-100 dark:[color-scheme:dark]";

function summary(day: WeekdayInfo, value: Deadline): string {
  const weekday = DAY_NAMES[(day.index - value.daysBefore + 49) % 7];
  const hours = String(Math.floor(value.localMinutes / 60)).padStart(2, "0");
  const minutes = String(value.localMinutes % 60).padStart(2, "0");
  return `${weekday} ساعت ${`${hours}:${minutes}`.replace(/\d/g, (d) => "۰۱۲۳۴۵۶۷۸۹"[Number(d)])}`;
}

export default function PolicyRow({ day, value, onChange }: PolicyRowProps) {
  const timeRef = useRef<HTMLInputElement>(null);

  const handleTime = (raw: string) => {
    if (raw === "") return;
    onChange({ ...value, localMinutes: fromTimeValue(raw) });
  };

  const openPicker = () => {
    try {
      timeRef.current?.showPicker();
    } catch {
      timeRef.current?.focus();
    }
  };

  return (
    <li className="rounded-2xl border border-slate-200 bg-white p-4 dark:border-white/10 dark:bg-[#0c242f]">
      <div className="mb-3 flex items-center justify-between gap-3">
        <h3 className="text-base font-bold text-slate-900 dark:text-slate-100">
          {day.label}
        </h3>
        <span className="rounded-full bg-teal-500/10 px-3 py-1 text-xs font-medium text-teal-700 dark:text-teal-300">
          مهلت: {summary(day, value)}
        </span>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <select
          value={value.daysBefore}
          onChange={(event) =>
            onChange({ ...value, daysBefore: Number(event.target.value) })
          }
          aria-label={`روز مهلت ${day.label}`}
          className={`${controlClass} appearance-none ps-10 ${ARROW}`}
        >
          {DAY_OPTIONS.map((option) => (
            <option key={option} value={option}>
              {option === 1
                ? "یک روز قبل"
                : `${option.toLocaleString("fa-IR")} روز قبل`}
            </option>
          ))}
        </select>

        <input
          ref={timeRef}
          type="time"
          dir="ltr"
          required
          value={toTimeValue(value.localMinutes)}
          onClick={openPicker}
          onChange={(event) => handleTime(event.target.value)}
          aria-label={`ساعت مهلت ${day.label}`}
          className={controlClass}
        />
      </div>
    </li>
  );
}
