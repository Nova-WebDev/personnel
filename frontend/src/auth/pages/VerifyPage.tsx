import {
  useEffect,
  useRef,
  useState,
  type ClipboardEvent,
  type FormEvent,
  type KeyboardEvent,
} from "react";
import { Navigate, useLocation } from "react-router-dom";
import { faLock } from "@fortawesome/free-solid-svg-icons";
import { useSendCode } from "../hooks/useSendCode";
import { useVerifyCode } from "../hooks/useVerifyCode";
import { useTempPhoneStore } from "../store/useTempPhoneStore";
import AuthLayout from "../ui/AuthLayout";
import { primaryButtonClass } from "../ui/authStyles";
import { getErrorMessage, getSafeRedirect, normalizeDigits } from "../utils";

const CODE_LENGTH = 5;
const RESEND_SECONDS = 60;

function remainingSeconds(readyAt: number): number {
  return Math.max(0, Math.ceil((readyAt - Date.now()) / 1000));
}

function emptyDigits(): string[] {
  return Array<string>(CODE_LENGTH).fill("");
}

export default function VerifyPage() {
  const phone = useTempPhoneStore((state) => state.tempPhone);
  const clearTempPhone = useTempPhoneStore((state) => state.clearTempPhone);
  const { search } = useLocation();

  const verify = useVerifyCode();
  const resend = useSendCode();

  const [digits, setDigits] = useState<string[]>(emptyDigits);
  const [resendReadyAt, setResendReadyAt] = useState(
    () => Date.now() + RESEND_SECONDS * 1000,
  );
  const [timer, setTimer] = useState(RESEND_SECONDS);
  const inputs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    const interval = window.setInterval(
      () => setTimer(remainingSeconds(resendReadyAt)),
      500,
    );
    return () => window.clearInterval(interval);
  }, [resendReadyAt]);

  if (phone === "") {
    const redirect = getSafeRedirect(search);
    return (
      <Navigate
        to={
          redirect === null
            ? "/auth/phone"
            : `/auth/phone?redirect=${encodeURIComponent(redirect)}`
        }
        replace
      />
    );
  }

  const submit = (code: string) => {
    if (code.length !== CODE_LENGTH || verify.isPending) return;
    verify.mutate(
      { phoneNumber: phone, code },
      {
        onSuccess: () => clearTempPhone(),
        onError: () => {
          setDigits(emptyDigits());
          inputs.current[0]?.focus();
        },
      },
    );
  };

  const fill = (startIndex: number, raw: string) => {
    const incoming = normalizeDigits(raw).slice(0, CODE_LENGTH - startIndex);
    if (incoming === "") return;

    const next = [...digits];
    for (let i = 0; i < incoming.length; i++) {
      next[startIndex + i] = incoming[i];
    }
    setDigits(next);

    const nextIndex = Math.min(startIndex + incoming.length, CODE_LENGTH - 1);
    inputs.current[nextIndex]?.focus();

    if (next.every((digit) => digit !== "")) submit(next.join(""));
  };

  const handleKeyDown = (
    event: KeyboardEvent<HTMLInputElement>,
    index: number,
  ) => {
    if (event.key === "Backspace") {
      event.preventDefault();
      const next = [...digits];
      if (next[index] !== "") {
        next[index] = "";
        setDigits(next);
      } else if (index > 0) {
        next[index - 1] = "";
        setDigits(next);
        inputs.current[index - 1]?.focus();
      }
    } else if (event.key === "ArrowLeft" && index > 0) {
      inputs.current[index - 1]?.focus();
    } else if (event.key === "ArrowRight" && index < CODE_LENGTH - 1) {
      inputs.current[index + 1]?.focus();
    }
  };

  const handlePaste = (event: ClipboardEvent<HTMLInputElement>) => {
    event.preventDefault();
    fill(0, event.clipboardData.getData("text"));
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    submit(digits.join(""));
  };

  const handleResend = () => {
    resend.mutate(phone, {
      onSuccess: () => {
        setResendReadyAt(Date.now() + RESEND_SECONDS * 1000);
        setTimer(RESEND_SECONDS);
        setDigits(emptyDigits());
        inputs.current[0]?.focus();
      },
    });
  };

  const errorMessage =
    verify.error !== null
      ? getErrorMessage(verify.error, "کد نامعتبر است.")
      : resend.error !== null
        ? getErrorMessage(resend.error, "ارسال دوباره ناموفق بود.")
        : null;

  return (
    <AuthLayout icon={faLock}>
      <p className="mb-6 text-center text-sm text-slate-600 dark:text-slate-300">
        کد ۵ رقمی ارسال‌شده به{" "}
        <span
          dir="ltr"
          className="font-semibold text-teal-700 dark:text-teal-300"
        >
          {phone}
        </span>{" "}
        را وارد کنید
      </p>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div dir="ltr" className="flex justify-center gap-2 sm:gap-3">
          {digits.map((digit, index) => (
            <input
              key={index}
              ref={(element) => {
                inputs.current[index] = element;
              }}
              value={digit}
              autoFocus={index === 0}
              autoComplete={index === 0 ? "one-time-code" : "off"}
              inputMode="numeric"
              maxLength={CODE_LENGTH}
              aria-label={`رقم ${index + 1}`}
              onChange={(event) => fill(index, event.target.value)}
              onKeyDown={(event) => handleKeyDown(event, index)}
              onPaste={handlePaste}
              onFocus={(event) => event.target.select()}
              className="h-11 w-11 rounded-xl border border-slate-300 bg-white/80 text-center text-xl text-slate-900 transition focus:outline-none focus:ring-2 focus:ring-teal-500 sm:h-12 sm:w-12 dark:border-white/15 dark:bg-white/5 dark:text-slate-100"
            />
          ))}
        </div>

        <button
          type="submit"
          disabled={verify.isPending || digits.some((digit) => digit === "")}
          className={primaryButtonClass}
        >
          {verify.isPending ? "در حال بررسی..." : "تأیید"}
        </button>
      </form>

      <div className="mt-4 text-center">
        {timer > 0 ? (
          <p className="text-sm text-slate-600 dark:text-slate-300">
            ارسال دوباره‌ی کد تا{" "}
            <span className="font-semibold text-teal-700 dark:text-teal-300">
              {timer} ثانیه
            </span>{" "}
            دیگر
          </p>
        ) : (
          <button
            type="button"
            onClick={handleResend}
            disabled={resend.isPending}
            className="cursor-pointer text-sm font-semibold text-teal-700 transition hover:text-teal-600 disabled:cursor-not-allowed dark:text-teal-300 dark:hover:text-teal-200"
          >
            {resend.isPending ? "در حال ارسال..." : "ارسال دوباره"}
          </button>
        )}
      </div>

      {errorMessage !== null && (
        <p className="mt-4 text-center text-sm text-red-600 dark:text-red-400">
          {errorMessage}
        </p>
      )}
    </AuthLayout>
  );
}
