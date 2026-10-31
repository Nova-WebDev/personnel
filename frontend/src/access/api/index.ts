import api from "../../shared/lib/axios";
import type { Permission, PermissionInput } from "../types";

export function getPermissions() {
  return api.get<Permission[]>("/user/permissions");
}

export function setUserPermissions(
  userId: string,
  permissions: PermissionInput[],
) {
  return api.put(`/user/user/${userId}/permissions`, { permissions });
}

export function deleteUserPermissions(userId: string) {
  return api.delete(`/user/user/${userId}/permissions`);
}
