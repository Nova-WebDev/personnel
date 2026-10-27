import { useEffect, type ReactNode } from "react";
import { useLocation } from "react-router-dom";

import { bootstrapSession } from "../auth/session";
import { useSessionStore } from "../auth/store/useSessionStore";
import Loader from "../base/loading/Loader";

function isFullyPublicPath(path: string): boolean {
  return path.startsWith("/card");
}

export default function AppProviders({ children }: { children: ReactNode }) {
  const { pathname } = useLocation();
  const status = useSessionStore((state) => state.status);
  const isPublic = isFullyPublicPath(pathname);

  useEffect(() => {
    if (!isPublic) void bootstrapSession();
  }, [isPublic]);

  if (!isPublic && status === "unknown") {
    return <Loader />;
  }

  return children;
}
