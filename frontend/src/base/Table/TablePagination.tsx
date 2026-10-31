import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faAngleDoubleLeft,
  faChevronLeft,
  faChevronRight,
  faAngleDoubleRight,
} from "@fortawesome/free-solid-svg-icons";
import type { TablePaginationProps } from "./types";

export default function TablePagination({
  page,
  total,
  limit,
  onPageChange,
}: TablePaginationProps) {
  const totalPages = Math.max(1, Math.ceil(total / Math.max(1, limit)));

  const goFirst = () => onPageChange(1);
  const goPrev = () => onPageChange(Math.max(1, page - 1));
  const goNext = () => onPageChange(Math.min(totalPages, page + 1));
  const goLast = () => onPageChange(totalPages);

  const base =
    "inline-flex items-center justify-center rounded-lg border transition-colors duration-150 focus:outline-none focus:ring-2 focus:ring-teal-500/30";
  const enabled =
    "cursor-pointer bg-white dark:bg-[#0c242f] border-slate-300 dark:border-white/10 hover:bg-teal-50 dark:hover:bg-[#12384a] hover:border-teal-400";
  const disabled =
    "bg-white dark:bg-[#0c242f] border-slate-200 dark:border-white/10 cursor-not-allowed opacity-40";
  const txt = "text-slate-700 dark:text-slate-200";

  return (
    <nav dir="rtl" className="flex items-center gap-2" aria-label="pagination">
      <div className="items-center hidden gap-2 sm:flex">
        <button
          onClick={goFirst}
          disabled={page === 1}
          aria-label="first"
          className={`${base} text-sm px-3 py-2 ${page === 1 ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faAngleDoubleRight} />
        </button>

        <button
          onClick={goPrev}
          disabled={page === 1}
          aria-label="prev"
          className={`${base} px-3 text-sm py-2 ${page === 1 ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronRight} />
        </button>

        <div className="flex items-center gap-2 px-3 py-2 text-sm rounded-lg bg-teal-50 dark:bg-teal-400/10">
          <span className="font-semibold text-teal-700 dark:text-teal-300">
            {page}
          </span>
          <span className="text-slate-400">/</span>
          <span className="text-slate-600 dark:text-slate-300">
            {totalPages}
          </span>
        </div>

        <button
          onClick={goNext}
          disabled={page === totalPages}
          aria-label="next"
          className={`${base} px-3 text-sm py-2 ${page === totalPages ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronLeft} />
        </button>

        <button
          onClick={goLast}
          disabled={page === totalPages}
          aria-label="last"
          className={`${base} px-3 text-sm py-2 ${page === totalPages ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faAngleDoubleLeft} />
        </button>
      </div>

      <div className="flex items-center gap-2 sm:hidden">
        <button
          onClick={goPrev}
          disabled={page === 1}
          aria-label="prev"
          className={`${base} px-3 py-2 ${page === 1 ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronRight} />
        </button>

        <div className="px-3 py-2 text-sm text-center rounded-lg bg-teal-50 dark:bg-teal-400/10 min-w-22">
          <span className="text-teal-700 dark:text-teal-300">
            {page} / {totalPages}
          </span>
        </div>

        <button
          onClick={goNext}
          disabled={page === totalPages}
          aria-label="next"
          className={`${base} px-3 py-2 ${page === totalPages ? disabled : enabled} ${txt}`}
        >
          <FontAwesomeIcon icon={faChevronLeft} />
        </button>
      </div>
    </nav>
  );
}
