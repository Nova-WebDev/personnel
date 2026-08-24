import { useMutation } from "@tanstack/react-query";
import { createBranch } from "../api/branchApi";

export function useCreateBranch() {
  return useMutation({
    mutationFn: ({ name }) => createBranch(name),
  });
}
