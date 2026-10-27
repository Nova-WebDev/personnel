import { Link } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCompass, faHome, faRotate } from "@fortawesome/free-solid-svg-icons";

const actionClass =
  "inline-flex cursor-pointer items-center gap-2 rounded-xl border border-teal-300/60 bg-teal-500/10 px-6 py-3 font-medium text-slate-800 backdrop-blur-md transition hover:border-teal-400 hover:bg-teal-500/20 active:scale-95 dark:border-teal-400/20 dark:bg-teal-400/10 dark:text-slate-100 dark:hover:bg-teal-400/20";

export default function NotFound() {
  return (
    <div className="fixed inset-0 flex items-center justify-center overflow-hidden bg-cyan-50 dark:bg-[#06141b]">
      <div className="pointer-events-none absolute inset-0">
        <div
          className="absolute -left-32 -top-32 h-[55vmax] w-[55vmax] rounded-full opacity-50 blur-[90px] dark:opacity-30"
          style={{
            background:
              "radial-gradient(circle at 30% 30%, rgba(20,184,166,0.45), transparent 45%), radial-gradient(circle at 70% 70%, rgba(34,211,238,0.35), transparent 50%)",
          }}
        />
        <div
          className="absolute -bottom-32 -right-32 h-[50vmax] w-[50vmax] rounded-full opacity-45 blur-[80px] dark:opacity-25"
          style={{
            background:
              "radial-gradient(circle at 20% 20%, rgba(6,182,212,0.4), transparent 40%), radial-gradient(circle at 80% 80%, rgba(45,212,191,0.3), transparent 45%)",
          }}
        />
      </div>

      <div className="relative z-10 flex flex-col items-center gap-10 px-6">
        <div className="flex h-[clamp(180px,28vmin,240px)] w-[clamp(180px,28vmin,240px)] animate-float-soft items-center justify-center rounded-full border border-white/70 bg-white/50 shadow-[0_30px_80px_rgba(13,148,136,0.25)] backdrop-blur-xl dark:border-white/10 dark:bg-white/5 dark:shadow-[0_30px_80px_rgba(0,0,0,0.5)]">
          <FontAwesomeIcon
            icon={faCompass}
            className="text-[clamp(48px,10vmin,72px)] text-teal-600 drop-shadow-[0_10px_30px_rgba(20,184,166,0.5)] dark:text-teal-300"
          />
        </div>

        <div className="text-center">
          <h1 className="bg-gradient-to-r from-teal-500 to-cyan-500 bg-clip-text text-6xl font-extrabold tracking-tight text-transparent md:text-7xl dark:from-teal-300 dark:to-cyan-300">
            404
          </h1>
          <p className="mt-2 text-sm text-slate-600 md:text-base dark:text-slate-300">
            Page not found
          </p>
        </div>

        <div className="flex gap-4">
          <Link to="/" className={actionClass}>
            <FontAwesomeIcon icon={faHome} />
            Home
          </Link>

          <button
            type="button"
            onClick={() => window.location.reload()}
            className={actionClass}
          >
            <FontAwesomeIcon icon={faRotate} />
            Retry
          </button>
        </div>
      </div>
    </div>
  );
}
