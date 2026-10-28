import { Navigate, Outlet } from "react-router-dom";

import { hasAnyLevel } from "../permissions";
import { useMeStore } from "../store/useMeStore";
import type { PermissionLevel } from "../types";

export function RoleRoute({ allow }: { allow: PermissionLevel[] }) {
  const me = useMeStore((state) => state.me);
  return me !== null && hasAnyLevel(me, allow) ? (
    <Outlet />
  ) : (
    <Navigate to="/" replace />
  );
}
