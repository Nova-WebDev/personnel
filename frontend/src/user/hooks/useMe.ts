import { useQuery } from "@tanstack/react-query";
import { useEffect } from "react";

import { usePersonnelStore } from "../../personnel/store/usePersonnelStore";
import { getMe } from "../api";
import { useMeStore } from "../store/useMeStore";

export function useMe() {
  const setMe = useMeStore((state) => state.setMe);
  const clear = useMeStore((state) => state.clear);
  const upsertMe = usePersonnelStore((state) => state.upsertMe);

  const query = useQuery({
    queryKey: ["me"],
    queryFn: async () => (await getMe()).data,
  });

  useEffect(() => {
    if (query.data !== undefined) {
      setMe(query.data);
      upsertMe(query.data);
    }
  }, [query.data, setMe, upsertMe]);

  useEffect(() => clear, [clear]);

  return query;
}
