import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { getMeals } from "../api";
import { useMealStore } from "../store/useMealStore";

export function useMeals() {
  const isComplete = useMealStore((state) => state.isComplete);
  const meals = useMealStore((state) => state.meals);
  const setAll = useMealStore((state) => state.setAll);

  const query = useQuery({
    queryKey: ["meals"],
    queryFn: async () => (await getMeals()).data,
    enabled: !isComplete,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data !== undefined) setAll(query.data);
  }, [query.data, setAll]);

  return {
    meals: Object.values(meals),
    isLoading: !isComplete && query.isLoading,
    isError: query.isError,
  };
}
