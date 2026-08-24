import api from "../../shared/lib/axios";

export function createBranch(name) {
  return api.post("/personnel/branches", { name });
}

export function updateBranch(branchId, name) {
  return api.put(`/personnel/branches/${branchId}`, { name });
}

export function deleteBranch(branchId) {
  return api.delete(`/personnel/branches/${branchId}`);
}

export function createUnit(name, branchId) {
  return api.post("/personnel/units", { name, branch_id: branchId });
}

export function updateUnitName(unitId, name) {
  return api.put(`/personnel/units/${unitId}`, { name });
}

export function deleteUnit(unitId) {
  return api.delete(`/personnel/units/${unitId}`);
}

export function getAllBranches() {
  return api.get("/personnel/branches");
}