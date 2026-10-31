import api from "../../shared/lib/axios";

export function getQrCode(userId: string) {
  return api.get<Blob>(`/user/user/${userId}/qrcode`, { responseType: "blob" });
}
