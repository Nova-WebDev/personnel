import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { getMe } from "../api";
import { useMeStore } from "../store/useMeStore";

export function useMe() {
  const setMe = useMeStore((state) => state.setMe);
  const clear = useMeStore((state) => state.clear);

  const query = useQuery({
    queryKey: ["me"],
    queryFn: async () => (await getMe()).data,
  });

  useEffect(() => {
    if (query.data !== undefined) setMe(query.data);
  }, [query.data, setMe]);

  useEffect(() => clear, [clear]);

  return query;
}
