import { faDownload } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import Loader from "../../base/loading/Loader";
import { useQrCode } from "../../profile/hooks/useQrCode";
import type { Personnel } from "../types";

interface QrModalContentProps {
  user: Personnel;
}

export default function QrModalContent({ user }: QrModalContentProps) {
  const { url, isLoading, isError } = useQrCode(user.id);

  return (
    <div className="flex flex-col items-center gap-4 p-6">
      <p className="font-semibold text-gray-800 dark:text-gray-100">
        {user.first_name} {user.last_name}
      </p>

      <div className="flex h-56 w-56 items-center justify-center rounded-xl bg-white p-3 ring-1 ring-slate-200">
        {isLoading && <Loader fullscreen={false} size={10} />}
        {isError && (
          <p className="text-center text-sm text-red-600">
            دریافت QR ناموفق بود.
          </p>
        )}
        {url !== null && (
          <img src={url} alt="QR" className="h-full w-full object-contain" />
        )}
      </div>

      {url !== null && (
        <a
          href={url}
          download={`qr-${user.personnel_code ?? user.id}.png`}
          className="flex h-10 w-full items-center justify-center gap-2 rounded-lg border border-teal-600 text-sm font-medium text-teal-700 transition hover:bg-teal-50 dark:border-teal-400/60 dark:text-teal-300 dark:hover:bg-teal-400/10"
        >
          <FontAwesomeIcon icon={faDownload} />
          دانلود تصویر
        </a>
      )}
    </div>
  );
}
