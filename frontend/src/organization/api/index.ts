import api from "../../shared/lib/axios";
import type { Branch } from "../types";

export function getBranches() {
  return api.get<Branch[]>("/user/branches");
}

export function createBranch(name: string) {
  return api.post("/user/branch", { name });
}

export function createUnit(name: string, branchId: string) {
  return api.post("/user/unit", { name, branch_id: branchId });
}
