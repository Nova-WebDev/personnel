import {
  faBuilding,
  faIdBadge,
  faIdCard,
  faMobileScreen,
  faSitemap,
  faShieldHalved,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import Avatar from "../../shared/ui/Avatar";
import { useMeStore } from "../../user/store/useMeStore";
import InfoRow from "../components/InfoRow";
import QrCard from "../components/QrCard";
import RoleBadges from "../components/RoleBadges";

export default function ProfilePage() {
  const me = useMeStore((state) => state.me);

  if (me === null) return null;

  const fullName = `${me.first_name} ${me.last_name}`.trim();
  const joined = new Date(me.created_at).toLocaleDateString("fa-IR");

  return (
    <div className="space-y-6">
      <section className="relative overflow-hidden rounded-2xl border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-[#0c242f]">
        <div className="absolute inset-x-0 top-0 h-24 bg-linear-to-l from-teal-600 to-cyan-600 dark:from-teal-700 dark:to-cyan-800" />

        <div className="relative flex flex-col items-center gap-4 pt-8 sm:flex-row sm:items-end sm:gap-6">
          <Avatar
            id={me.id}
            photoPath={me.photo_path}
            className="h-28 w-28 shrink-0 !ring-4 !ring-white dark:!ring-[#0c242f]"
          />
          <div className="flex-1 text-center sm:pb-2 sm:text-start">
            <h1 className="text-2xl font-extrabold text-slate-900 dark:text-slate-100">
              {fullName}
            </h1>
            <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
              {[me.unit_name, me.branch_name].filter(Boolean).join(" · ") ||
                "بدون واحد"}
            </p>
          </div>
          <span
            className={`rounded-full px-3 py-1 text-xs font-semibold sm:mb-2 ${
              me.is_blocked
                ? "bg-red-100 text-red-700 dark:bg-red-500/15 dark:text-red-300"
                : "bg-emerald-100 text-emerald-700 dark:bg-emerald-400/15 dark:text-emerald-300"
            }`}
          >
            {me.is_blocked ? "مسدود" : "فعال"}
          </span>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-3">
        <div className="space-y-6 lg:col-span-2">
          <section className="rounded-2xl border border-slate-200 bg-white px-6 py-2 dark:border-white/10 dark:bg-[#0c242f]">
            <div className="divide-y divide-slate-100 dark:divide-white/10">
              <InfoRow icon={faMobileScreen} label="شماره موبایل">
                <span dir="ltr">{me.phone}</span>
              </InfoRow>
              <InfoRow icon={faIdBadge} label="کد پرسنلی">
                {me.personnel_code ?? "—"}
              </InfoRow>
              <InfoRow icon={faSitemap} label="سازمان">
                {me.branch_name ?? "—"}
              </InfoRow>
              <InfoRow icon={faBuilding} label="واحد">
                {me.unit_name ?? "—"}
              </InfoRow>
              <InfoRow icon={faIdCard} label="کارت RFID">
                {me.rfid_card_id === null ? "ثبت نشده" : "ثبت شده"}
              </InfoRow>
              <InfoRow icon={faIdBadge} label="تاریخ عضویت">
                {joined}
              </InfoRow>
            </div>
          </section>

          <section className="space-y-3 rounded-2xl border border-slate-200 bg-white p-6 dark:border-white/10 dark:bg-[#0c242f]">
            <h2 className="flex items-center gap-2 font-bold text-slate-900 dark:text-slate-100">
              <FontAwesomeIcon
                icon={faShieldHalved}
                className="text-teal-600 dark:text-teal-300"
              />
              دسترسی‌های من
            </h2>
            <RoleBadges scopes={me.scopes} />
          </section>
        </div>

        <QrCard userId={me.id} />
      </div>
    </div>
  );
}
