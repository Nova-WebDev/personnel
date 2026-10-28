import { faBars, faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";
import { Outlet } from "react-router-dom";

import Loader from "../../base/loading/Loader";
import Avatar from "../../shared/ui/Avatar";
import { useMe } from "../../user/hooks/useMe";
import { useMeStore } from "../../user/store/useMeStore";
import Sidebar from "./Sidebar";

export default function MainLayout() {
  const [open, setOpen] = useState(false);
  const { isError, refetch } = useMe();
  const me = useMeStore((state) => state.me);

  if (me === null) {
    if (!isError) return <Loader />;

    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-slate-100 dark:bg-[#06141b]">
        <p className="text-slate-600 dark:text-slate-300">
          دریافت اطلاعات کاربر ناموفق بود.
        </p>
        <button
          type="button"
          onClick={() => void refetch()}
          className="cursor-pointer rounded-lg bg-teal-600 px-5 py-2 font-medium text-white transition hover:bg-teal-700"
        >
          تلاش دوباره
        </button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-slate-100 dark:bg-[#06141b]">
      <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b border-slate-200 bg-white/90 px-4 backdrop-blur lg:hidden dark:border-white/10 dark:bg-[#0a1f29]/90">
        <button
          type="button"
          onClick={() => setOpen(true)}
          aria-label="باز کردن منو"
          className="flex h-10 w-10 cursor-pointer items-center justify-center rounded-lg text-slate-600 transition hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-white/10"
        >
          <FontAwesomeIcon icon={faBars} />
        </button>
        <span className="flex-1 font-semibold text-teal-700 dark:text-teal-300">
          سامانه پرسنل و غذا
        </span>
        <Avatar id={me.id} photoPath={me.photo_path} className="h-9 w-9" />
      </header>

      <div
        onClick={() => setOpen(false)}
        className={`fixed inset-0 z-40 bg-black/40 transition-opacity lg:hidden ${
          open ? "opacity-100" : "pointer-events-none opacity-0"
        }`}
      />

      <aside
        className={`fixed inset-y-0 start-0 z-50 w-72 border-e border-slate-200 bg-white transition-transform duration-200 lg:w-64 dark:border-white/10 dark:bg-[#0a1f29] ${
          open ? "" : "max-lg:ltr:-translate-x-full max-lg:rtl:translate-x-full"
        }`}
      >
        <button
          type="button"
          onClick={() => setOpen(false)}
          aria-label="بستن منو"
          className="absolute end-3 top-4 z-10 hidden h-8 w-8 cursor-pointer items-center justify-center rounded-lg text-slate-400 max-lg:flex"
        >
          <FontAwesomeIcon icon={faXmark} />
        </button>
        <Sidebar me={me} onNavigate={() => setOpen(false)} />
      </aside>

      <main className="p-4 sm:p-6 lg:ms-64">
        <Outlet />
      </main>
    </div>
  );
}
