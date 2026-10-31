import type { TableBodyProps } from "./types";

const cellClass = `
  px-4 py-4 align-middle whitespace-nowrap text-center
  bg-white dark:bg-[#0c242f]
  text-slate-800 dark:text-slate-100
  border-y border-slate-200 dark:border-white/10
  transition-colors duration-200
  group-hover:bg-teal-50 dark:group-hover:bg-[#12384a]
`;

export default function TableBody<T>({
  data,
  columns,
  actions,
  mode,
}: TableBodyProps<T>) {
  if (mode === "desktop") {
    return (
      <>
        {data.map((row, idx) => (
          <tr key={idx} className="group">
            {columns.map((col, i) => (
              <td
                key={i}
                className={`${cellClass} first:rounded-s-xl first:border-s`}
              >
                <div className="flex h-12 items-center justify-center">
                  {col.render(row)}
                </div>
              </td>
            ))}

            {actions && (
              <td className={`${cellClass} last:rounded-e-xl last:border-e`}>
                <div className="flex h-12 items-center justify-center gap-2">
                  {actions.map((action, i) => (
                    <div key={i}>{action.render(row)}</div>
                  ))}
                </div>
              </td>
            )}
          </tr>
        ))}
      </>
    );
  }

  return (
    <div className="pt-3 space-y-4 md:hidden">
      {data.map((row, idx) => (
        <article
          key={idx}
          className="
            bg-white dark:bg-[#0c242f]
            border border-slate-200 dark:border-white/10
            rounded-2xl p-4
            shadow-sm
            transition-all duration-200
            hover:shadow-md
            hover:border-teal-300 dark:hover:border-teal-400/40
            focus-within:border-teal-400
            flex flex-col gap-3
            ring-0 outline-none
          "
          tabIndex={0}
        >
          {columns.map((col, i) => (
            <div
              key={i}
              className="flex flex-col items-center gap-1 px-1 py-0.5 text-center"
              aria-label={`field-${col.label.toLowerCase().replace(/\s+/g, "-")}`}
            >
              <div className="text-[11px] leading-4 text-teal-700 dark:text-teal-300">
                {col.label}
              </div>

              <div className="flex items-center justify-center p-2 text-sm font-normal leading-5 text-slate-800 wrap-break-word dark:text-slate-100">
                {col.render(row)}
              </div>

              {i !== columns.length - 1 && (
                <div className="w-full h-px mt-2 bg-slate-200 dark:bg-white/10" />
              )}
            </div>
          ))}

          {actions && (
            <div className="flex flex-col gap-2 pt-2 mt-1 border-t border-slate-200 dark:border-white/10">
              {actions.map((action, i) => (
                <div key={i} className="w-full">
                  {action.render(row)}
                </div>
              ))}
            </div>
          )}
        </article>
      ))}
    </div>
  );
}
