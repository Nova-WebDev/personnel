import { useState, useRef, useEffect } from "react";
import { useTempPhoneStore } from "../store/useTempPhoneStore";
import { useVerifyCode } from "../hooks/useVerifyCode";
import { useSendCode } from "../hooks/useSendCode";
import Cookies from "js-cookie";
import { decodeJWT } from "../../shared/utils/jwt";
import { useUserStore } from "../../auth/store/useUserStore";
import { useNavigate } from "react-router-dom";
import { navigateWithRules } from "../../shared/utils/navigateWithRules";

export default function VerifyPage() {
  const phone = useTempPhoneStore((s) => s.tempPhone);
  const clearTempPhone = useTempPhoneStore((s) => s.clearTempPhone);

  const { mutate: verifyMutate, isPending, error } = useVerifyCode();
  const { mutate: resendMutate, isPending: isResending } = useSendCode();

  const setUserFromToken = useUserStore((s) => s.setUserFromToken);

  const navigate = useNavigate();
  const navigateRef = useRef(navigate);

  const [code, setCode] = useState(["", "", "", "", ""]);
  const inputsRef = useRef([]);
  const [timer, setTimer] = useState(60);

  const url = new URL(window.location.href);
  const redirect = url.searchParams.get("redirect");

  useEffect(() => {
    if (timer === 0) return;
    const interval = setInterval(() => setTimer((t) => t - 1), 1000);
    return () => clearInterval(interval);
  }, [timer]);

  const handleResend = () => {
    resendMutate({ phone_number: phone });
    setTimer(60);
  };

  const handleChange = (value, index) => {
    if (!/^[0-9]?$/.test(value)) return;
    const newCode = [...code];
    newCode[index] = value;
    setCode(newCode);
    if (value && index < 4) inputsRef.current[index + 1].focus();
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && !code[index] && index > 0) {
      inputsRef.current[index - 1].focus();
    }
  };

  const go = (path) => {
    if (redirect) {
      navigateWithRules(
        navigateRef.current,
        `${path}?redirect=${encodeURIComponent(redirect)}`,
      );
    } else {
      navigateWithRules(navigateRef.current, path);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const finalCode = code.join("");
    verifyMutate(
      { phone_number: phone, code: finalCode },
      {
        onSuccess: (data) => {
          const { access_token, refresh_token } = data.data;
          localStorage.setItem("refresh_token", refresh_token);
          Cookies.set("access_token", access_token, {
            secure: false,
            sameSite: "lax",
          });
          const decoded = decodeJWT(access_token);
          setUserFromToken({
            phone_number: phone,
            public_id: decoded.public_id,
            role: decoded.role,
            exp: decoded.exp,
          });
          clearTempPhone();
          go("/");
        },
      },
    );
  };

  return (
    <div className="flex items-center justify-center min-h-screen px-4 transition-colors bg-gray-100 sm:px-6 dark:bg-gray-900">
      <div className="w-full max-w-sm mx-auto overflow-hidden bg-white border border-gray-200 shadow-lg sm:max-w-md dark:bg-gray-800 dark:border-gray-700 rounded-xl">
        <div className="h-1.5 bg-indigo-700 dark:bg-indigo-500"></div>

        <div className="p-6 sm:p-8">
          <h1 className="mb-2 text-3xl font-semibold text-center text-indigo-700 dark:text-indigo-400">
            تأیید کد
          </h1>

          <p className="mb-6 text-sm text-center text-gray-600 dark:text-gray-300">
            کد ۵ رقمی ارسال شده به
            <span className="font-semibold text-indigo-700 dark:text-indigo-400">
              {" "}
              {phone}
            </span>
          </p>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex justify-center gap-2 sm:gap-4">
              {code.map((char, index) => (
                <input
                  key={index}
                  ref={(el) => (inputsRef.current[index] = el)}
                  maxLength={1}
                  value={char}
                  inputMode="numeric"
                  pattern="[0-9]*"
                  onChange={(e) => handleChange(e.target.value, index)}
                  onKeyDown={(e) => handleKeyDown(e, index)}
                  className="w-10 h-10 text-xl text-center border border-gray-300 rounded-md sm:w-12 sm:h-12 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-600"
                />
              ))}
            </div>

            <button
              type="submit"
              disabled={isPending}
              className="w-full py-3 rounded-md bg-indigo-700 hover:bg-indigo-800 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white font-semibold tracking-wide transition active:scale-[0.98] disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
            >
              {isPending ? "در حال بررسی..." : "تأیید"}
            </button>
          </form>

          <div className="mt-4 text-center">
            {timer > 0 ? (
              <p className="text-sm text-gray-600 dark:text-gray-300">
                می‌توانید دوباره کد را ارسال کنید در{" "}
                <span className="font-semibold text-indigo-700 dark:text-indigo-400">
                  {timer} ثانیه
                </span>
              </p>
            ) : (
              <button
                onClick={handleResend}
                disabled={isResending}
                className="text-sm font-semibold text-indigo-700 transition cursor-pointer hover:text-indigo-800 dark:text-indigo-400 dark:hover:text-indigo-300 disabled:cursor-not-allowed"
              >
                {isResending ? "در حال ارسال..." : "ارسال دوباره"}
              </button>
            )}
          </div>

          {error && (
            <p className="mt-4 text-sm text-center text-red-600 dark:text-red-400">
              {error.message || "کد نامعتبر است."}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}