export interface WeekdayInfo {
  key: string;
  label: string;
  index: number;
}

export const WEEK: WeekdayInfo[] = [
  { key: "saturday", label: "شنبه", index: 6 },
  { key: "sunday", label: "یکشنبه", index: 0 },
  { key: "monday", label: "دوشنبه", index: 1 },
  { key: "tuesday", label: "سه‌شنبه", index: 2 },
  { key: "wednesday", label: "چهارشنبه", index: 3 },
  { key: "thursday", label: "پنجشنبه", index: 4 },
  { key: "friday", label: "جمعه", index: 5 },
];

export const MAX_DAYS_BEFORE = 6;
const DAY = 1440;

export interface Deadline {
  daysBefore: number;
  localMinutes: number;
}

function offsetMinutes(): number {
  return -new Date().getTimezoneOffset();
}

function mod(value: number, base: number): number {
  return ((value % base) + base) % base;
}

export function encodeCutoff({ daysBefore, localMinutes }: Deadline): string {
  const utcMinutes = mod(localMinutes - offsetMinutes(), DAY);
  const total = daysBefore * DAY - (utcMinutes === 0 ? DAY : utcMinutes);
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
}

export function decodeCutoff(cutoff: string): Deadline {
  const [hours, minutes] = cutoff.split(":").map(Number);
  const total = (hours || 0) * 60 + (minutes || 0);
  const daysBefore = Math.min(MAX_DAYS_BEFORE, Math.floor(total / DAY) + 1);
  const utcMinutes = daysBefore * DAY - total;
  return { daysBefore, localMinutes: mod(utcMinutes + offsetMinutes(), DAY) };
}

const digits = "۰۱۲۳۴۵۶۷۸۹";

export function formatMinutes(total: number): string {
  const text = `${String(Math.floor(total / 60)).padStart(2, "0")}:${String(total % 60).padStart(2, "0")}`;
  return text.replace(/\d/g, (digit) => digits[Number(digit)]);
}

export function toTimeValue(total: number): string {
  return `${String(Math.floor(total / 60)).padStart(2, "0")}:${String(total % 60).padStart(2, "0")}`;
}

export function fromTimeValue(value: string): number {
  const [hours, minutes] = value.split(":").map(Number);
  return (hours || 0) * 60 + (minutes || 0);
}
