import { useMutation } from "@tanstack/react-query";
import { setPersonnelBlockStatus } from "../api/personnelApi";

export function useSetPersonnelBlockStatus() {
  return useMutation({
    mutationFn: ({ personnelUuid, isBlocked }) =>
      setPersonnelBlockStatus(personnelUuid, isBlocked),
  });
}
