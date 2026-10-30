import { useMutation } from "@tanstack/react-query";

import { cancelReservation, reserveMeal } from "../api";
import { useMealPlanStore } from "../store/useMealPlanStore";

export function useReserve() {
  const plans = useMealPlanStore((state) => state.plans);
  const setReserved = useMealPlanStore((state) => state.setReserved);

  return useMutation({
    mutationFn: async (planId: string) => {
      const plan = plans[planId];
      if (plan?.is_reserved) await cancelReservation(planId);
      else await reserveMeal(planId);
    },
    onSuccess: (_data, planId) => {
      const plan = plans[planId];
      if (plan === undefined) return;
      for (const other of Object.values(plans)) {
        if (
          other.plan_date === plan.plan_date &&
          other.id !== planId &&
          other.is_reserved
        ) {
          setReserved(other.id, false);
        }
      }
      setReserved(planId, !plan.is_reserved);
    },
  });
}
