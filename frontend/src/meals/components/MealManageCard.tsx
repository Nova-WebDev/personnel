import { faBan, faLockOpen, faPen } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

import DefaultMealImage from "../../shared/ui/DefaultMealImage";
import type { Meal } from "../types";

interface MealManageCardProps {
  meal: Meal;
  pending: boolean;
  onEdit: () => void;
  onToggle: () => void;
}

export default function MealManageCard({
  meal,
  pending,
  onEdit,
  onToggle,
}: MealManageCardProps) {
  const [failed, setFailed] = useState(false);
  const hasPhoto = meal.photo_path !== null && !failed;

  return (
    <article
      className={`flex flex-col gap-3 rounded-2xl border border-slate-200 bg-white p-3 transition dark:border-white/10 dark:bg-[#0c242f] ${
        meal.is_active ? "" : "opacity-60"
      }`}
    >
      <div className="flex gap-3">
        <div className="relative h-24 w-24 shrink-0 overflow-hidden rounded-xl">
          {hasPhoto ? (
            <img
              src={`/api/meals/meal/${meal.id}/photo`}
              alt=""
              loading="lazy"
              onError={() => setFailed(true)}
              className="h-full w-full object-cover"
            />
          ) : (
            <DefaultMealImage className="h-full w-full" />
          )}
        </div>

        <div className="min-w-0 flex-1">
          <div className="flex items-start justify-between gap-2">
            <h3 className="truncate font-bold text-slate-900 dark:text-slate-100">
              {meal.title}
            </h3>
            {!meal.is_active && (
              <span className="shrink-0 rounded-full bg-slate-900/80 px-2 py-0.5 text-[10px] font-semibold text-white">
                غیرفعال
              </span>
            )}
          </div>
          {meal.description !== null && meal.description !== "" && (
            <p className="mt-1 line-clamp-3 text-sm text-slate-500 dark:text-slate-400">
              {meal.description}
            </p>
          )}
        </div>
      </div>

      <div className="flex gap-2">
        <button
          type="button"
          dir="ltr"
          onClick={onEdit}
          className="flex h-9 flex-1 cursor-pointer items-center justify-center gap-2 rounded-lg border border-slate-300 text-xs font-medium text-slate-700 transition hover:bg-slate-100 dark:border-white/15 dark:text-slate-200 dark:hover:bg-white/10"
        >
          <FontAwesomeIcon icon={faPen} />
          Edit
        </button>
        <button
          type="button"
          dir="ltr"
          onClick={onToggle}
          disabled={pending}
          className={`flex h-9 flex-1 cursor-pointer items-center justify-center gap-2 rounded-lg border text-xs font-medium transition disabled:cursor-not-allowed disabled:opacity-60 ${
            meal.is_active
              ? "border-red-300 text-red-600 hover:bg-red-50 dark:border-red-400/40 dark:text-red-400 dark:hover:bg-red-500/10"
              : "border-emerald-300 text-emerald-600 hover:bg-emerald-50 dark:border-emerald-400/40 dark:text-emerald-400 dark:hover:bg-emerald-500/10"
          }`}
        >
          <FontAwesomeIcon icon={meal.is_active ? faBan : faLockOpen} />
          {meal.is_active ? "Deactivate" : "Activate"}
        </button>
      </div>
    </article>
  );
}
