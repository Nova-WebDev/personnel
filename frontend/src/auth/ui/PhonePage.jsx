import { useState, useEffect, useRef } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPhone, faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { useSendCode } from "../hooks/useSendCode";
import { useTempPhoneStore } from "../store/useTempPhoneStore";
import { useNavigate } from "react-router-dom";
import { navigateWithRules } from "../../shared/utils/navigateWithRules";

export default function PhonePage() {
  const [phone, setPhone] = useState("");
  const { mutate, isPending, isSuccess, error } = useSendCode();

  const setTempPhone = useTempPhoneStore((s) => s.setTempPhone);
  const navigate = useNavigate();

  const navigateRef = useRef(navigate);
  const setTempPhoneRef = useRef(setTempPhone);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (/^09\d{9}$/.test(phone)) {
      mutate({ phone_number: phone });
    }
  };

  useEffect(() => {
    if (isSuccess) {
      setTempPhoneRef.current(phone);
      const url = new URL(window.location.href);
      const redirect = url.searchParams.get("redirect");
      if (redirect) {
        navigateWithRules(
          navigateRef.current,
          `/auth/verify?redirect=${encodeURIComponent(redirect)}`
        );
      } else {
        navigateWithRules(navigateRef.current, "/auth/verify");
      }
    }
  }, [isSuccess, phone]);

  return (
    <div className="flex items-center justify-center min-h-screen px-4 transition-colors bg-gray-100 sm:px-6 dark:bg-gray-900">
      <div className="w-full max-w-sm mx-auto overflow-hidden bg-white border border-gray-200 shadow-lg sm:max-w-md dark:bg-gray-800 dark:border-gray-700 rounded-xl">
        <div className="h-1.5 bg-indigo-700 dark:bg-indigo-500"></div>

        <div className="p-6 sm:p-8">
          <h1 className="mb-6 text-3xl font-semibold text-center text-indigo-700 dark:text-indigo-400">
            ورود با موبایل
          </h1>

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block mb-1 text-sm text-gray-600 dark:text-gray-300">
                شماره موبایل
              </label>
              <div className="relative">
                <span className="absolute text-gray-500 -translate-y-1/2 left-3 top-1/2 dark:text-gray-400">
                  <FontAwesomeIcon icon={faPhone} className="w-5 h-5" />
                </span>
                <input
                  type="tel"
                  required
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="09xxxxxxxxx"
                  pattern="^09\d{9}$"
                  className="w-full py-3 pr-4 text-gray-900 placeholder-gray-400 transition border border-gray-300 rounded-md pl-11 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 dark:text-gray-100 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-600"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isPending}
              className="w-full py-3 cursor-pointer rounded-md bg-indigo-700 hover:bg-indigo-800 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white font-semibold tracking-wide transition active:scale-[0.98] disabled:opacity-60 flex items-center justify-center gap-2"
            >
              <FontAwesomeIcon icon={faPaperPlane} className="w-4 h-4" />
              {isPending ? "در حال ارسال..." : "ارسال کد"}
            </button>
          </form>

          {error && (
            <p className="mt-4 text-sm text-center text-red-600 dark:text-red-400">
              {error.message || "مشکلی پیش آمد."}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}