import { useMutation } from "@tanstack/react-query";
import { deleteBranch } from "../api/branchApi";

export function useDeleteBranch() {
  return useMutation({
    mutationFn: ({ branchId }) => deleteBranch(branchId),
  });
}
