import { getPersonnelPhotoUrl } from "../api/personnelApi";

export function useGetPersonnelPhotoUrl(fileId) {
  return getPersonnelPhotoUrl(fileId);
}
