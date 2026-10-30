import { useEffect, useState } from "react";

import { serverNow } from "../../shared/time/useTimeStore";

export function useNow(intervalMs = 30_000): number {
  const [now, setNow] = useState(serverNow);

  useEffect(() => {
    const id = window.setInterval(() => setNow(serverNow()), intervalMs);
    return () => window.clearInterval(id);
  }, [intervalMs]);

  return now;
}
