export type RoleKey = "ADMIN" | "KITCHEN" | "GROUP_MANAGER" | "HR_MANAGER";

export interface Permission {
  permission_id: string;
  user_id: string;
  first_name: string;
  last_name: string;
  level: string;
  unit_id: string | null;
  unit_name: string | null;
  branch_id: string | null;
  branch_name: string | null;
}

export interface PermissionInput {
  level: string;
  scope: string | null;
}

export interface AddPermissionInput {
  user_id: string;
  level: RoleKey;
  unit_id: string | null;
}

export interface RoleInfo {
  key: RoleKey;
  label: string;
  scoped: boolean;
  locked: boolean;
}

export const ROLES: RoleInfo[] = [
  { key: "ADMIN", label: "ادمین", scoped: false, locked: true },
  { key: "KITCHEN", label: "آشپز", scoped: false, locked: false },
  { key: "GROUP_MANAGER", label: "مدیر گروه", scoped: true, locked: false },
  { key: "HR_MANAGER", label: "منابع انسانی", scoped: true, locked: false },
];
