import { useMutation } from "@tanstack/react-query";
import { updatePersonnel } from "../api/personnelApi";

export function useUpdatePersonnel() {
  return useMutation({
    mutationFn: ({ personnelUuid, ...payload }) =>
      updatePersonnel(personnelUuid, payload),
  });
}
