import { useMutation } from "@tanstack/react-query";
import { deleteUnit } from "../api/branchApi";

export function useDeleteUnit() {
  return useMutation({
    mutationFn: ({ unitId }) => deleteUnit(unitId),
  });
}
