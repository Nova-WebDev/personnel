import { faArrowLeft, faUtensils } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Link } from "react-router-dom";

import { useMeStore } from "../../user/store/useMeStore";

export default function HomePage() {
  const me = useMeStore((state) => state.me);

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-white/5">
        <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
          سلام {me?.first_name}
        </h1>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          برای هر روز غذای خود را انتخاب کنید.
        </p>
      </div>

      <Link
        to="/meals"
        className="flex items-center justify-between rounded-2xl border border-teal-500/20 bg-teal-500/10 p-5 text-teal-700 transition hover:bg-teal-500/15 dark:text-teal-300"
      >
        <span className="flex items-center gap-3 font-medium">
          <FontAwesomeIcon icon={faUtensils} />
          رزرو غذا
        </span>
        <FontAwesomeIcon icon={faArrowLeft} />
      </Link>
    </div>
  );
}
