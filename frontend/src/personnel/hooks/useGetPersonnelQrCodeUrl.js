import { getPersonnelQrCodeUrl } from "../api/personnelApi";

export function useGetPersonnelQrCodeUrl(personnelUuid) {
  return getPersonnelQrCodeUrl(personnelUuid);
}
