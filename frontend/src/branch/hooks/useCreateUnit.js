import { useMutation } from "@tanstack/react-query";
import { createUnit } from "../api/branchApi";

export function useCreateUnit() {
  return useMutation({
    mutationFn: ({ name, branchId }) => createUnit(name, branchId),
  });
}
