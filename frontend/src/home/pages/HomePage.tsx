import { useMemo, useState } from "react";

import Loader from "../../base/loading/Loader";
import { useReserve } from "../../meals/hooks/useReserve";
import { useTimePolicies } from "../../meals/hooks/useTimePolicies";
import { useWeekPlans } from "../../meals/hooks/useWeekPlans";
import {
  addDays,
  deadlineMs,
  todayUtc,
  weekdayOf,
} from "../../meals/utils/dates";
import DayPicker from "../components/DayPicker";
import DeadlineBanner from "../components/DeadlineBanner";
import MealCard from "../components/MealCard";
import { useNow } from "../hooks/useNow";

const DAYS_AHEAD = 7;

export default function HomePage() {
  const today = todayUtc();
  const now = useNow(10_000);

  const days = useMemo(
    () =>
      Array.from({ length: DAYS_AHEAD }, (_, index) => addDays(today, index)),
    [today],
  );
  const [selected, setSelected] = useState(days[1] ?? days[0]);

  const { plans, isLoading, isError } = useWeekPlans(
    days[0],
    days[DAYS_AHEAD - 1],
  );
  const policies = useTimePolicies();
  const reserve = useReserve();

  const reservedDays = useMemo(
    () =>
      new Set(
        plans.filter((plan) => plan.is_reserved).map((plan) => plan.plan_date),
      ),
    [plans],
  );
  const dayPlans = plans.filter((plan) => plan.plan_date === selected);

  const cutoff =
    policies.find(
      (policy) => policy.target_weekday.toLowerCase() === weekdayOf(selected),
    )?.cutoff_before ?? "0:00";
  const deadline = deadlineMs(selected, cutoff);
  const locked = deadline - now <= 0;

  return (
    <div className="space-y-6">
      <DayPicker
        days={days}
        selected={selected}
        reservedDays={reservedDays}
        today={today}
        onSelect={setSelected}
      />

      {!locked && <DeadlineBanner deadline={deadline} />}

      {isLoading && <Loader fullscreen={false} size={12} />}
      {isError && (
        <p className="text-red-600 dark:text-red-400">
          دریافت برنامه ناموفق بود.
        </p>
      )}

      {!isLoading && !isError && dayPlans.length === 0 && (
        <div className="rounded-2xl border border-dashed border-slate-300 p-10 text-center text-slate-500 dark:border-white/15 dark:text-slate-400">
          برای این روز غذایی تعریف نشده است.
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {dayPlans.map((plan) => (
          <MealCard
            key={plan.id}
            plan={plan}
            locked={locked}
            pending={reserve.isPending}
            onToggle={() => reserve.mutate(plan.id)}
          />
        ))}
      </div>
    </div>
  );
}
