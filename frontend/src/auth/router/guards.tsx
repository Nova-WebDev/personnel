import { Navigate, Outlet } from "react-router-dom";

import { useSessionStore } from "../store/useSessionStore";

export function ProtectedRoute() {
  const status = useSessionStore((state) => state.status);
  return status === "authenticated" ? (
    <Outlet />
  ) : (
    <Navigate to="/auth/phone" replace />
  );
}

export function PublicOnlyRoute() {
  const status = useSessionStore((state) => state.status);
  return status === "authenticated" ? <Navigate to="/" replace /> : <Outlet />;
}
