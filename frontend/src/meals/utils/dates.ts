import { serverNow } from "../../shared/time/useTimeStore";

const WEEKDAYS = [
  "sunday",
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
  "saturday",
];

export function toIso(date: Date): string {
  return date.toISOString().slice(0, 10);
}

export function addDays(iso: string, days: number): string {
  const date = new Date(`${iso}T00:00:00Z`);
  date.setUTCDate(date.getUTCDate() + days);
  return toIso(date);
}

export function todayUtc(): string {
  return toIso(new Date(serverNow()));
}

export function weekdayOf(iso: string): string {
  return WEEKDAYS[new Date(`${iso}T00:00:00Z`).getUTCDay()];
}

export function deadlineMs(planDate: string, cutoffHours: number): number {
  return new Date(`${planDate}T00:00:00Z`).getTime() - cutoffHours * 3_600_000;
}

const faDay = new Intl.DateTimeFormat("fa-IR", {
  weekday: "long",
  timeZone: "UTC",
});
const faShort = new Intl.DateTimeFormat("fa-IR", {
  day: "numeric",
  month: "long",
  timeZone: "UTC",
});

export function formatDay(iso: string): string {
  return faDay.format(new Date(`${iso}T00:00:00Z`));
}

export function formatShort(iso: string): string {
  return faShort.format(new Date(`${iso}T00:00:00Z`));
}

export function splitRemaining(ms: number): { days: number; clock: string } {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000));
  const days = Math.floor(totalSeconds / 86_400);
  const hours = Math.floor((totalSeconds % 86_400) / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;
  const pad = (value: number) => String(value).padStart(2, "0");

  return { days, clock: `${pad(hours)}:${pad(minutes)}:${pad(seconds)}` };
}
