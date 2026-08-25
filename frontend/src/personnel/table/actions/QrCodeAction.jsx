import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faQrcode } from "@fortawesome/free-solid-svg-icons";
import { useGetPersonnelQrCodeUrl } from "../../hooks/useGetPersonnelQrCodeUrl";

export function QrCodeAction({ row }) {
  const qrUrl = useGetPersonnelQrCodeUrl(row.uuid);

  return (
    <a
      href={qrUrl}
      target="_blank"
      rel="noreferrer"
      className="flex items-center justify-center w-full gap-2 py-2 pl-5 pr-3 text-sm text-white bg-indigo-600 rounded-md cursor-pointer md:w-auto hover:bg-indigo-700"
    >
      <FontAwesomeIcon icon={faQrcode} />
      QR Code
    </a>
  );
}