import { faClock } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { splitRemaining } from "../../meals/utils/dates";
import { useNow } from "../hooks/useNow";

interface DeadlineBannerProps {
  deadline: number;
}

export default function DeadlineBanner({ deadline }: DeadlineBannerProps) {
  const now = useNow(1000);
  const remainingMs = deadline - now;
  const urgent = remainingMs < 6 * 3_600_000;
  const { days, clock } = splitRemaining(remainingMs);

  return (
    <div
      className={`flex items-center gap-3 rounded-xl border px-4 py-3 text-sm ${
        urgent
          ? "border-amber-300 bg-amber-50 text-amber-800 dark:border-amber-400/30 dark:bg-amber-400/10 dark:text-amber-300"
          : "border-slate-200 bg-white text-slate-600 dark:border-white/10 dark:bg-[#0c242f] dark:text-slate-300"
      }`}
    >
      <FontAwesomeIcon icon={faClock} />
      <span>
        مهلت انتخاب برای این روز:{" "}
        {days > 0 && <strong>{days.toLocaleString("fa-IR")} روز و </strong>}
        <strong dir="ltr" className="inline-block tabular-nums">
          {clock}
        </strong>
      </span>
    </div>
  );
}
