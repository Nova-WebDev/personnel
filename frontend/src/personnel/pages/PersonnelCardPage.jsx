import { useParams } from "react-router-dom";

import NotFound from "../../shared/ui/NotFound";
import Loader from "../../base/loading/Loader";
import { useGetPersonnelDetail } from "../hooks/useGetPersonnelDetail";
import { useGetPersonnelPhotoUrl } from "../hooks/useGetPersonnelPhotoUrl";
import { POSITION_OPTIONS } from "../constants/positionOptions";
import defaultProfile from "../../shared/assets/photo/profile.png";

export const PersonnelCardPage = () => {
  const { uuid } = useParams();
  const { data, isLoading, error } = useGetPersonnelDetail(uuid);

  const personnel = data?.data;

  const fileId = personnel?.photo_path
    ? personnel.photo_path.split("/").pop()
    : null;
  const photoUrl = useGetPersonnelPhotoUrl(fileId);

  if (isLoading) {
    return <Loader />;
  }

  if (error || !personnel || personnel.is_blocked) {
    return <NotFound />;
  }

  const positionLabel = POSITION_OPTIONS.find(
    (opt) => opt.value === personnel.position,
  )?.label;

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#F5F6FD] dark:bg-[#0b1020] px-4 py-10">
      <div
        className="
          w-full max-w-sm
          bg-white dark:bg-[#111a2b]
          rounded-3xl shadow-xl
          border border-indigo-100 dark:border-indigo-500/10
          overflow-hidden
        "
      >
        <div className="relative h-24 bg-indigo-600 dark:bg-indigo-700">
          <div className="absolute -translate-x-1/2 -bottom-12 left-1/2">
            <img
              src={fileId ? photoUrl : defaultProfile}
              alt={`${personnel.first_name} ${personnel.last_name}`}
              className="w-24 h-24 rounded-full object-cover border-4 border-white dark:border-[#111a2b] shadow-md"
            />
          </div>
        </div>

        <div className="px-6 pt-16 pb-8 text-center">
          <h1 className="text-xl font-bold text-gray-800 dark:text-gray-100">
            {personnel.first_name} {personnel.last_name}
          </h1>

          <p className="mt-1 text-sm text-indigo-600 dark:text-indigo-400">
            {positionLabel || "—"}
          </p>

          <div className="mt-6 space-y-3 text-right" dir="rtl">
            <InfoRow label="شماره پرسنلی" value={personnel.personnel_id} />
            <InfoRow label="شرکت" value={personnel.branch_name} />
            <InfoRow label="واحد" value={personnel.unit_name} />
          </div>
        </div>
      </div>
    </div>
  );
};

function InfoRow({ label, value }) {
  return (
    <div className="flex items-center justify-between px-4 py-3 rounded-xl bg-indigo-50 dark:bg-indigo-500/10">
      <span className="text-xs text-gray-500 dark:text-gray-400">{label}</span>
      <span className="text-sm font-medium text-gray-800 dark:text-gray-100">
        {value || "—"}
      </span>
    </div>
  );
}