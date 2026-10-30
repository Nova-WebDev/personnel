import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { getServerTime } from "./api";
import { useTimeStore } from "./useTimeStore";

export function useServerClock() {
  const isComplete = useTimeStore((state) => state.isComplete);
  const setServerTime = useTimeStore((state) => state.setServerTime);

  const query = useQuery({
    queryKey: ["server-time"],
    queryFn: async () => (await getServerTime()).data.server_time,
    enabled: !isComplete,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data !== undefined) setServerTime(query.data);
  }, [query.data, setServerTime]);

  return isComplete;
}
