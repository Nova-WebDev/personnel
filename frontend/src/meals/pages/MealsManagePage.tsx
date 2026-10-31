import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

import Loader from "../../base/loading/Loader";
import Modal from "../../base/Modal";
import MealForm from "../components/MealForm";
import MealManageCard from "../components/MealManageCard";
import { useMeals } from "../hooks/useMeals";
import { useSetMealActive } from "../hooks/useSetMealActive";
import type { Meal } from "../types";

type ActiveModal = { kind: "create" } | { kind: "edit"; meal: Meal } | null;

export default function MealsManagePage() {
  const [active, setActive] = useState<ActiveModal>(null);
  const { meals, isLoading, isError } = useMeals();
  const setActiveStatus = useSetMealActive();

  const close = () => setActive(null);
  const sorted = [...meals].sort(
    (a, b) =>
      Number(b.is_active) - Number(a.is_active) ||
      a.title.localeCompare(b.title, "fa"),
  );

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={() => setActive({ kind: "create" })}
          className="flex h-11 cursor-pointer items-center gap-2 rounded-lg bg-teal-600 px-5 text-sm font-medium text-white transition hover:bg-teal-700"
        >
          <FontAwesomeIcon icon={faPlus} />
          افزودن غذا
        </button>
        {!isLoading && !isError && (
          <span className="text-sm text-slate-500 dark:text-slate-400">
            {meals.length.toLocaleString("fa-IR")} غذا
          </span>
        )}
      </div>

      {isLoading && <Loader fullscreen={false} size={12} />}
      {isError && (
        <p className="text-red-600 dark:text-red-400">
          دریافت غذاها ناموفق بود.
        </p>
      )}

      {!isLoading && !isError && sorted.length === 0 && (
        <div className="rounded-2xl border border-dashed border-slate-300 p-10 text-center text-slate-500 dark:border-white/15 dark:text-slate-400">
          هنوز غذایی ثبت نشده است.
        </div>
      )}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
        {sorted.map((meal) => (
          <MealManageCard
            key={meal.id}
            meal={meal}
            pending={setActiveStatus.isPending}
            onEdit={() => setActive({ kind: "edit", meal })}
            onToggle={() =>
              setActiveStatus.mutate({ id: meal.id, isActive: !meal.is_active })
            }
          />
        ))}
      </div>

      <Modal
        open={active !== null}
        title={active?.kind === "edit" ? "ویرایش غذا" : "افزودن غذا"}
        onClose={close}
      >
        {active?.kind === "create" && <MealForm onDone={close} />}
        {active?.kind === "edit" && (
          <MealForm key={active.meal.id} initial={active.meal} onDone={close} />
        )}
      </Modal>
    </div>
  );
}
