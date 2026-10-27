import axios from "axios";

const PERSIAN_DIGITS = "۰۱۲۳۴۵۶۷۸۹";
const ARABIC_DIGITS = "٠١٢٣٤٥٦٧٨٩";

export function normalizeDigits(value: string): string {
  return value
    .replace(/[۰-۹]/g, (d) => String(PERSIAN_DIGITS.indexOf(d)))
    .replace(/[٠-٩]/g, (d) => String(ARABIC_DIGITS.indexOf(d)))
    .replace(/\D/g, "");
}

export function getSafeRedirect(search: string): string | null {
  const redirect = new URLSearchParams(search).get("redirect");
  return redirect !== null &&
    redirect.startsWith("/") &&
    !redirect.startsWith("//")
    ? redirect
    : null;
}

export function getErrorMessage(error: unknown, fallback: string): string {
  if (axios.isAxiosError(error)) {
    const detail: unknown = error.response?.data?.detail;
    if (typeof detail === "string") return detail;
    if (error.response === undefined) return "ارتباط با سرور برقرار نشد.";
  }
  return fallback;
}
