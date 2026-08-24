import { useMutation } from "@tanstack/react-query";
import { createPersonnel } from "../api/personnelApi";

export function useCreatePersonnel() {
  return useMutation({
    mutationFn: (payload) => createPersonnel(payload),
  });
}
