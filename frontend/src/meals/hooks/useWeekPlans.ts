import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { getMealPlans } from "../api";
import { useMealPlanStore } from "../store/useMealPlanStore";

export function useWeekPlans(from: string, to: string) {
  const isComplete = useMealPlanStore((state) => state.isComplete);
  const loadedFrom = useMealPlanStore((state) => state.loadedFrom);
  const loadedTo = useMealPlanStore((state) => state.loadedTo);
  const plans = useMealPlanStore((state) => state.plans);
  const setRange = useMealPlanStore((state) => state.setRange);

  const covered =
    isComplete &&
    loadedFrom !== null &&
    loadedTo !== null &&
    loadedFrom <= from &&
    loadedTo >= to;

  const query = useQuery({
    queryKey: ["meal-plans", from, to],
    queryFn: async () => (await getMealPlans(from, to)).data,
    enabled: !covered,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data !== undefined) setRange(query.data, from, to);
  }, [query.data, from, to, setRange]);

  return {
    plans: Object.values(plans).filter(
      (plan) => plan.plan_date >= from && plan.plan_date <= to,
    ),
    isLoading: !covered && query.isLoading,
    isError: query.isError,
  };
}
