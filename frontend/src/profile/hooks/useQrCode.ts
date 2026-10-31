import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import { getQrCode } from "../api";

export function useQrCode(userId: string) {
  const [url, setUrl] = useState<string | null>(null);

  const query = useQuery({
    queryKey: ["qrcode", userId],
    queryFn: async () => (await getQrCode(userId)).data,
    staleTime: Infinity,
  });

  useEffect(() => {
    if (query.data === undefined) return;
    const objectUrl = URL.createObjectURL(query.data);
    setUrl(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [query.data]);

  return { url, isLoading: query.isLoading, isError: query.isError };
}
