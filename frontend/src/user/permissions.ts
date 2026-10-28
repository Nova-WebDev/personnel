import type { Me, PermissionLevel } from "./types";

export function hasAnyLevel(me: Me, allowed?: PermissionLevel[]): boolean {
  if (allowed === undefined) return true;

  const levels = me.scopes.map((scope) => scope.level.toLowerCase());
  return (
    levels.includes("admin") || allowed.some((level) => levels.includes(level))
  );
}
