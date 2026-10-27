import type { ReactNode } from "react";

import { cardClass } from "./authStyles";

export default function AuthLayout({
  title,
  children,
}: {
  title: string;
  children: ReactNode;
}) {
  return (
    <div className="relative flex min-h-screen items-center justify-center overflow-hidden bg-slate-100 px-4 sm:px-6 dark:bg-[#06141b]">
      <div className="pointer-events-none absolute inset-0 hidden dark:block">
        <div
          className="absolute -left-32 -top-32 h-[55vmax] w-[55vmax] rounded-full opacity-30 blur-[90px]"
          style={{
            background:
              "radial-gradient(circle at 30% 30%, rgba(20,184,166,0.45), transparent 45%), radial-gradient(circle at 70% 70%, rgba(34,211,238,0.35), transparent 50%)",
          }}
        />
        <div
          className="absolute -bottom-32 -right-32 h-[50vmax] w-[50vmax] rounded-full opacity-25 blur-[80px]"
          style={{
            background:
              "radial-gradient(circle at 20% 20%, rgba(6,182,212,0.4), transparent 40%), radial-gradient(circle at 80% 80%, rgba(45,212,191,0.3), transparent 45%)",
          }}
        />
      </div>

      <div className={`relative z-10 ${cardClass}`}>
        <div className="h-1.5 bg-linear-to-r from-teal-500 to-cyan-500" />
        <div className="p-6 sm:p-8">
          <h1 className="mb-6 text-center text-3xl font-semibold text-teal-700 dark:text-teal-300">
            {title}
          </h1>
          {children}
        </div>
      </div>
    </div>
  );
}
