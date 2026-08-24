import { useMutation } from "@tanstack/react-query";
import { updateUnitName } from "../api/branchApi";

export function useUpdateUnitName() {
  return useMutation({
    mutationFn: ({ unitId, name }) => updateUnitName(unitId, name),
  });
}
