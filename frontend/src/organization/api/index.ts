import api from "../../shared/lib/axios";
import type { Branch } from "../types";

export function getBranches() {
  return api.get<Branch[]>("/user/branches");
}

export function createBranch(name: string) {
  return api.post("/user/branch", { name });
}

export function updateBranch(branchId: string, name: string) {
  return api.patch(`/user/branch/${branchId}`, { name });
}

export function deleteBranch(branchId: string) {
  return api.delete(`/user/branch/${branchId}`);
}

export function createUnit(name: string, branchId: string) {
  return api.post("/user/unit", { name, branch_id: branchId });
}

export function updateUnit(unitId: string, name: string) {
  return api.patch(`/user/unit/${unitId}`, { name });
}

export function deleteUnit(unitId: string) {
  return api.delete(`/user/unit/${unitId}`);
}
