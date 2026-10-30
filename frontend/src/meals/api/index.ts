import api from "../../shared/lib/axios";
import type { MealPlan, TimePolicy } from "../types";

export function getMealPlans(dateFrom: string, dateTo: string) {
  return api.get<MealPlan[]>("/meals/meal-plan", {
    params: { date_from: dateFrom, date_to: dateTo },
  });
}

export function getTimePolicies() {
  return api.get<TimePolicy[]>("/meals/meal-plan-time-policies");
}

export function reserveMeal(mealPlanId: string) {
  return api.post("/meals/voucher", { meal_plan_id: mealPlanId });
}

export function cancelReservation(mealPlanId: string) {
  return api.delete(`/meals/voucher/${mealPlanId}`);
}
