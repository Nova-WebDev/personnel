import { useState } from "react";
import { Outlet } from "react-router-dom";

import Loader from "../../base/loading/Loader";
import { useServerClock } from "../../shared/time/useServerClock";
import { useMe } from "../../user/hooks/useMe";
import { useMeStore } from "../../user/store/useMeStore";
import Header from "./Header";
import Sidebar from "./Sidebar";

export default function MainLayout() {
  const [open, setOpen] = useState(false);
  const { isError, refetch } = useMe();
  const clockReady = useServerClock();
  const me = useMeStore((state) => state.me);

  if (me === null || !clockReady) {
    if (!isError) return <Loader />;

    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-slate-100 dark:bg-[#06141b]">
        <p className="text-slate-600 dark:text-slate-300">
          دریافت اطلاعات کاربر ناموفق بود.
        </p>
        <button
          type="button"
          onClick={() => void refetch()}
          className="cursor-pointer rounded-lg bg-teal-600 px-5 py-2.5 font-medium text-white transition hover:bg-teal-700"
        >
          تلاش دوباره
        </button>
      </div>
    );
  }

  return (
    <div
      dir="rtl"
      className="min-h-screen bg-linear-to-br from-slate-200 via-slate-100 to-cyan-50 dark:from-[#06141b] dark:via-[#071a22] dark:to-[#06141b]"
    >
      <Header me={me} onMenu={() => setOpen(true)} />

      <div
        onClick={() => setOpen(false)}
        className={`fixed inset-0 z-40 bg-black/50 transition-opacity lg:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
      />

      <aside
        className={`fixed bottom-0 right-0 top-0 z-50 w-64 border-l border-slate-200 bg-white transition-transform duration-200 dark:border-white/10 dark:bg-[#0c242f] lg:bottom-3 lg:right-3 lg:top-[88px] lg:z-30 lg:translate-x-0 lg:rounded-2xl lg:border lg:border-slate-300 lg:shadow-[0_2px_8px_rgba(15,23,42,0.08)] dark:lg:border-white/10 dark:lg:shadow-none ${
          open ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <Sidebar me={me} onNavigate={() => setOpen(false)} />
      </aside>

      <main className="px-3 pb-6 pt-[89px] lg:mr-[17rem] lg:pl-3">
        <Outlet />
      </main>
    </div>
  );
}
