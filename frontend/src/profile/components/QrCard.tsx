import { faDownload, faQrcode } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import Loader from "../../base/loading/Loader";
import { useQrCode } from "../hooks/useQrCode";

export default function QrCard({ userId }: { userId: string }) {
  const { url, isLoading, isError } = useQrCode(userId);

  return (
    <section className="flex flex-col items-center gap-4 rounded-2xl border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-[#0c242f]">
      <h2 className="flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
        <FontAwesomeIcon
          icon={faQrcode}
          className="text-teal-600 dark:text-teal-300"
        />
        کد QR من
      </h2>

      <div className="flex h-52 w-52 items-center justify-center rounded-xl bg-white p-3 ring-1 ring-slate-200">
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
          download="qr-code.png"
          className="flex h-10 w-full items-center justify-center gap-2 rounded-lg border border-teal-600 text-sm font-medium text-teal-700 transition hover:bg-teal-50 dark:border-teal-400/60 dark:text-teal-300 dark:hover:bg-teal-400/10"
        >
          <FontAwesomeIcon icon={faDownload} />
          دانلود تصویر
        </a>
      )}
    </section>
  );
}
