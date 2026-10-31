import type { Me, PermissionLevel } from "./types";

export interface Access {
  isAdmin: boolean;
  hrUnitIds: Set<string> | null;
}

export function hasAnyLevel(me: Me, allowed?: PermissionLevel[]): boolean {
  if (allowed === undefined) return true;

  const levels = me.scopes.map((scope) => scope.level.toLowerCase());
  return (
    levels.includes("admin") || allowed.some((level) => levels.includes(level))
  );
}

export function computeAccess(me: Me): Access {
  const isAdmin = me.scopes.some(
    (scope) => scope.level.toLowerCase() === "admin",
  );
  if (isAdmin) return { isAdmin: true, hrUnitIds: null };

  const unitIds = me.scopes
    .filter(
      (scope) =>
        scope.level.toLowerCase() === "hr_manager" && scope.unit_id !== null,
    )
    .map((scope) => scope.unit_id as string);

  return { isAdmin: false, hrUnitIds: new Set(unitIds) };
}

export function isUnitAllowed(
  hrUnitIds: Set<string> | null | undefined,
  unitId: string | null,
): boolean {
  if (hrUnitIds === null) return true;
  if (hrUnitIds === undefined) return false;
  return unitId !== null && hrUnitIds.has(unitId);
}
