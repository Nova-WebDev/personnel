import { faClock } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { useNow } from "../../home/hooks/useNow";

const format = new Intl.DateTimeFormat("fa-IR", {
  hour: "2-digit",
  minute: "2-digit",
  second: "2-digit",
  hour12: false,
  timeZone: "UTC",
});

export default function ServerClock() {
  const now = useNow(1000);

  return (
    <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
      <FontAwesomeIcon
        icon={faClock}
        className="text-teal-600 dark:text-teal-300"
      />
      ساعت سرور (UTC):
      <strong dir="ltr" className="tabular-nums">
        {format.format(new Date(now))}
      </strong>
    </div>
  );
}
