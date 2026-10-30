import { faPaperPlane, faPhone } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState, type ChangeEvent, type FormEvent } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { useSendCode } from "../hooks/useSendCode";
import { useTempPhoneStore } from "../store/useTempPhoneStore";
import AuthLayout from "../ui/AuthLayout";
import { primaryButtonClass } from "../ui/authStyles";
import { getErrorMessage, getSafeRedirect, normalizeDigits } from "../utils";

const PHONE_PATTERN = /^09\d{9}$/;

export default function PhonePage() {
  const [phone, setPhone] = useState("");
  const [touched, setTouched] = useState(false);

  const navigate = useNavigate();
  const { search } = useLocation();
  const setTempPhone = useTempPhoneStore((state) => state.setTempPhone);
  const { mutate, isPending, error } = useSendCode();

  const isValid = PHONE_PATTERN.test(phone);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setPhone(normalizeDigits(event.target.value).slice(0, 11));
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    setTouched(true);
    if (!isValid || isPending) return;

    mutate(phone, {
      onSuccess: () => {
        setTempPhone(phone);
        const redirect = getSafeRedirect(search);
        navigate(
          redirect === null
            ? "/auth/verify"
            : `/auth/verify?redirect=${encodeURIComponent(redirect)}`,
        );
      },
    });
  };

  return (
    <AuthLayout title="ورود با موبایل" icon={faPhone}>
      <form onSubmit={handleSubmit} className="space-y-5" noValidate>
        <div>
          <label
            htmlFor="phone"
            className="mb-1 block text-sm text-end text-slate-600 dark:text-slate-300"
          >
            شماره موبایل
          </label>
          <div className="relative">
            <span className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-teal-600 dark:text-teal-300">
              <FontAwesomeIcon icon={faPhone} className="h-5 w-5" />
            </span>
            <input
              id="phone"
              type="tel"
              inputMode="numeric"
              autoComplete="tel"
              autoFocus
              dir="ltr"
              value={phone}
              onChange={handleChange}
              placeholder="09xxxxxxxxx"
              className="w-full rounded-xl border border-slate-300 bg-white/80 py-3 pl-11 pr-4 text-slate-900 placeholder-slate-400 transition focus:outline-none focus:ring-2 focus:ring-teal-500 dark:border-white/15 dark:bg-white/5 dark:text-slate-100 dark:placeholder-slate-500"
            />
          </div>
          {touched && !isValid && (
            <p className="mt-2 text-sm text-red-600 dark:text-red-400">
              شماره موبایل باید با ۰۹ شروع شود و ۱۱ رقم باشد.
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isPending}
          className={primaryButtonClass}
        >
          <FontAwesomeIcon icon={faPaperPlane} className="h-4 w-4" />
          {isPending ? "در حال ارسال..." : "ارسال کد"}
        </button>
      </form>

      {error !== null && (
        <p className="mt-4 text-center text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(error, "مشکلی پیش آمد.")}
        </p>
      )}
    </AuthLayout>
  );
}
