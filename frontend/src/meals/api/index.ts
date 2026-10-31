import api from "../../shared/lib/axios";
import axiosMultipart from "../../shared/lib/axiosMultipart";
import type { CreateMealInput, Meal, MealPlan, TimePolicy } from "../types";

function toFormData(input: CreateMealInput): FormData {
  const form = new FormData();
  form.append("title", input.title);
  if (input.description !== "") form.append("description", input.description);
  if (input.photo !== null) form.append("photo", input.photo);
  return form;
}

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

export function getMeals() {
  return api.get<Meal[]>("/meals/meal");
}

export function createMeal(input: CreateMealInput) {
  return axiosMultipart.post("/meals/meal", toFormData(input));
}

export function updateMeal(id: string, input: CreateMealInput) {
  return axiosMultipart.patch(`/meals/meal/${id}`, toFormData(input));
}

export function setMealActive(id: string, isActive: boolean) {
  return api.patch(`/meals/meal/${id}/active-status`, { is_active: isActive });
}
