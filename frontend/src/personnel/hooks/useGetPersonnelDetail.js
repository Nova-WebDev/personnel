import { useQuery } from "@tanstack/react-query";
import { getPersonnelDetail } from "../api/personnelApi";

export function useGetPersonnelDetail(personnelUuid) {
  return useQuery({
    queryKey: ["personnel-detail", personnelUuid],
    queryFn: () => getPersonnelDetail(personnelUuid),
    enabled: !!personnelUuid,
  });
}
