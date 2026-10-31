import api from "../../shared/lib/axios";

export interface TimePolicyInput {
  target_weekday: string;
  cutoff_before: string;
}

export function setTimePolicies(policies: TimePolicyInput[]) {
  return api.put("/meals/meal-plan-time-policies", { policies });
}
