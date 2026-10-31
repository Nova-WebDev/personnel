export interface Meal {
  id: string;
  title: string;
  description: string | null;
  photo_path: string | null;
  is_active: boolean;
}

export interface MealPlan {
  id: string;
  plan_date: string;
  meal: Meal;
  is_reserved: boolean;
}

export interface TimePolicy {
  id: string;
  target_weekday: string;
  cutoff_before: string;
}

export interface CreateMealInput {
  title: string;
  description: string;
  photo: File | null;
}
