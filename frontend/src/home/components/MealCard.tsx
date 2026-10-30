import { faCheck, faLock } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import type { MealPlan } from "../../meals/types";

interface MealCardProps {
  plan: MealPlan;
  locked: boolean;
  pending: boolean;
  onToggle: () => void;
}

export default function MealCard({
  plan,
  locked,
  pending,
  onToggle,
}: MealCardProps) {
  const { meal } = plan;
  const reserved = plan.is_reserved;

  return (
    <div
      className={`overflow-hidden rounded-2xl border transition ${
        reserved
          ? "border-teal-500 bg-teal-50 dark:border-teal-400/60 dark:bg-teal-400/10"
          : "border-slate-200 bg-white dark:border-white/10 dark:bg-[#0c242f]"
      }`}
    >
      <div className="relative aspect-[16/10] bg-slate-100 dark:bg-white/5">
        {meal.photo_path !== null && (
          <img
            src={`/api/meals/meal/${meal.id}/photo`}
            alt=""
            loading="lazy"
            className="h-full w-full object-cover"
          />
        )}
        {reserved && (
          <span className="absolute start-3 top-3 flex items-center gap-1.5 rounded-full bg-teal-600 px-3 py-1 text-xs font-semibold text-white">
            <FontAwesomeIcon icon={faCheck} />
            انتخاب شما
          </span>
        )}
      </div>

      <div className="space-y-3 p-4">
        <div>
          <h3 className="font-bold text-slate-900 dark:text-slate-100">
            {meal.title}
          </h3>
          {meal.description !== null && (
            <p className="mt-1 line-clamp-2 text-sm text-slate-500 dark:text-slate-400">
              {meal.description}
            </p>
          )}
        </div>

        <button
          type="button"
          onClick={onToggle}
          disabled={locked || pending}
          className={`flex h-11 w-full cursor-pointer items-center justify-center gap-2 rounded-xl text-sm font-semibold transition disabled:cursor-not-allowed ${
            locked
              ? "bg-slate-100 text-slate-400 dark:bg-white/5 dark:text-slate-500"
              : reserved
                ? "border border-red-300 text-red-600 hover:bg-red-50 dark:border-red-400/40 dark:text-red-400 dark:hover:bg-red-500/10"
                : "bg-teal-600 text-white hover:bg-teal-700"
          }`}
        >
          {locked && <FontAwesomeIcon icon={faLock} />}
          {locked ? "مهلت تمام شده" : reserved ? "لغو رزرو" : "انتخاب این غذا"}
        </button>
      </div>
    </div>
  );
}
