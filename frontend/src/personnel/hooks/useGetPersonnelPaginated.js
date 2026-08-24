import { useQuery } from "@tanstack/react-query";
import { getPersonnelPaginated } from "../api/personnelApi";

export function useGetPersonnelPaginated(params) {
  return useQuery({
    queryKey: ["personnel", params],
    queryFn: () => getPersonnelPaginated(params),
  });
}
