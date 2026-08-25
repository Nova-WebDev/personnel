import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChevronDown,
  faBuilding,
  faPlus,
  faPen,
  faTrash,
} from "@fortawesome/free-solid-svg-icons";
import Swal from "sweetalert2";
import { UnitRow } from "./UnitRow";
import { CreateUnitModal } from "../CreateUnitModal";
import { EditBranchModal } from "../EditBranchModal";
import { useDeleteBranch } from "../../hooks/useDeleteBranch";
import { useBranchesStore } from "../../store/useBranchesStore";

export function BranchRow({ branch }) {
  const [open, setOpen] = useState(false);
  const [openCreateUnitModal, setOpenCreateUnitModal] = useState(false);
  const [openEditBranchModal, setOpenEditBranchModal] = useState(false);

  const deleteBranchMutation = useDeleteBranch();
  const removeBranch = useBranchesStore((state) => state.removeBranch);

  const unitCount = branch.units?.length || 0;
  const isDarkMode = document.documentElement.classList.contains("dark");

  const handleDelete = async () => {
    const result = await Swal.fire({
      title: "حذف شرکت",
      html: `<div dir="rtl">آیا مطمئن هستید که می‌خواهید شرکت <b>${branch.name}</b> را حذف کنید؟</div>`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "بله، حذف شود",
      cancelButtonText: "انصراف",
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      background: isDarkMode ? "#141b30" : "#ffffff",
      color: isDarkMode ? "#e5e7eb" : "#111111",
    });

    if (!result.isConfirmed) return;

    try {
      await deleteBranchMutation.mutateAsync({ branchId: branch.id });
      removeBranch(branch.id);

      Swal.fire({
        title: "حذف شد!",
        html: `<div dir="rtl">شرکت <b>${branch.name}</b> با موفقیت حذف گردید.</div>`,
        icon: "success",
        confirmButtonText: "باشه",
        background: isDarkMode ? "#141b30" : "#ffffff",
        color: isDarkMode ? "#e5e7eb" : "#111111",
      });
    } catch (err) {
      console.error("Error deleting branch:", err);
      Swal.fire({
        title: "خطا",
        html: `<div dir="rtl">خطا در حذف شرکت <b>${branch.name}</b> رخ داد.</div>`,
        icon: "error",
        confirmButtonText: "باشه",
        background: isDarkMode ? "#141b30" : "#ffffff",
        color: isDarkMode ? "#e5e7eb" : "#111111",
      });
    }
  };

  return (
    <>
      <li className="rounded-2xl border bg-[#f0f1fb] dark:bg-[#141b30] border-indigo-200 dark:border-[#232f52] transition-all duration-200">
        <div
          className="flex items-center justify-between gap-2 p-4 cursor-pointer select-none"
          onClick={() => setOpen(!open)}
        >
          <div className="flex items-center gap-3 min-w-0">
            <div className="flex items-center justify-center text-indigo-600 bg-indigo-100 w-9 h-9 rounded-xl dark:bg-indigo-500/10 dark:text-indigo-400 shrink-0">
              <FontAwesomeIcon icon={faBuilding} className="text-sm" />
            </div>
            <div className="min-w-0">
              <div className="font-semibold text-gray-800 dark:text-gray-100 truncate">
                {branch.name}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">
                {unitCount} واحد
              </div>
            </div>
          </div>

          <div className="flex items-center gap-1 shrink-0">
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setOpenCreateUnitModal(true);
              }}
              className="flex items-center justify-center w-8 h-8 rounded-lg text-gray-500 hover:text-indigo-600 hover:bg-indigo-100 dark:text-gray-400 dark:hover:text-indigo-400 dark:hover:bg-indigo-500/10 transition-colors cursor-pointer"
            >
              <FontAwesomeIcon icon={faPlus} className="text-sm" />
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setOpenEditBranchModal(true);
              }}
              className="flex items-center justify-center w-8 h-8 rounded-lg text-gray-500 hover:text-indigo-600 hover:bg-indigo-100 dark:text-gray-400 dark:hover:text-indigo-400 dark:hover:bg-indigo-500/10 transition-colors cursor-pointer"
            >
              <FontAwesomeIcon icon={faPen} className="text-sm" />
            </button>
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                handleDelete();
              }}
              className="flex items-center justify-center w-8 h-8 rounded-lg text-gray-500 hover:text-red-600 hover:bg-red-50 dark:text-gray-400 dark:hover:text-red-400 dark:hover:bg-red-500/10 transition-colors cursor-pointer"
            >
              <FontAwesomeIcon icon={faTrash} className="text-sm" />
            </button>

            <div className="w-px h-5 mx-1 bg-indigo-200 dark:bg-indigo-500/20" />

            <FontAwesomeIcon
              icon={faChevronDown}
              className={`text-gray-500 dark:text-gray-400 transition-transform duration-300 ${
                open ? "rotate-180" : ""
              }`}
            />
          </div>
        </div>

        {open && (
          <div className="px-4 pb-4">
            {unitCount === 0 ? (
              <div className="p-2.5 text-sm text-gray-500 dark:text-gray-400">
                واحدی برای این شرکت ثبت نشده است.
              </div>
            ) : (
              <ul className="space-y-2">
                {branch.units.map((unit) => (
                  <UnitRow key={unit.id} unit={unit} branchId={branch.id} />
                ))}
              </ul>
            )}
          </div>
        )}
      </li>

      {openCreateUnitModal && (
        <CreateUnitModal
          branchId={branch.id}
          onClose={() => setOpenCreateUnitModal(false)}
        />
      )}

      {openEditBranchModal && (
        <EditBranchModal
          branchId={branch.id}
          branchName={branch.name}
          onClose={() => setOpenEditBranchModal(false)}
        />
      )}
    </>
  );
}
