export default function PagePlaceholder({ title }: { title: string }) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-8 dark:border-white/10 dark:bg-white/5">
      <h1 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">
        {title}
      </h1>
    </div>
  );
}
