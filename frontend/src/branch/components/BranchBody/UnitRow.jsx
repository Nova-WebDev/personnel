import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faLayerGroup,
  faPen,
  faTrash,
} from "@fortawesome/free-solid-svg-icons";
import Swal from "sweetalert2";
import { EditUnitModal } from "../EditUnitModal";
import { useDeleteUnit } from "../../hooks/useDeleteUnit";
import { useBranchesStore } from "../../store/useBranchesStore";

export function UnitRow({ unit, branchId }) {
  const [openEditUnitModal, setOpenEditUnitModal] = useState(false);

  const deleteUnitMutation = useDeleteUnit();
  const removeUnit = useBranchesStore((state) => state.removeUnit);

  const isDarkMode = document.documentElement.classList.contains("dark");

  const handleDelete = async () => {
    const result = await Swal.fire({
      title: "حذف واحد",
      html: `<div dir="rtl">آیا مطمئن هستید که می‌خواهید واحد <b>${unit.name}</b> را حذف کنید؟</div>`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonText: "بله، حذف شود",
      cancelButtonText: "انصراف",
      confirmButtonColor: "#d33",
      cancelButtonColor: "#3085d6",
      background: isDarkMode ? "#1a2742" : "#ffffff",
      color: isDarkMode ? "#e5e7eb" : "#111111",
    });

    if (!result.isConfirmed) return;

    try {
      await deleteUnitMutation.mutateAsync({ unitId: unit.id });
      removeUnit(branchId, unit.id);

      Swal.fire({
        title: "حذف شد!",
        html: `<div dir="rtl">واحد <b>${unit.name}</b> با موفقیت حذف گردید.</div>`,
        icon: "success",
        confirmButtonText: "باشه",
        background: isDarkMode ? "#1a2742" : "#ffffff",
        color: isDarkMode ? "#e5e7eb" : "#111111",
      });
    } catch (err) {
      console.error("Error deleting unit:", err);
      Swal.fire({
        title: "خطا",
        html: `<div dir="rtl">خطا در حذف واحد <b>${unit.name}</b> رخ داد.</div>`,
        icon: "error",
        confirmButtonText: "باشه",
        background: isDarkMode ? "#1a2742" : "#ffffff",
        color: isDarkMode ? "#e5e7eb" : "#111111",
      });
    }
  };

  return (
    <>
      <li className="flex items-center justify-between gap-2 p-2.5 rounded-lg bg-white dark:bg-[#1a2742] border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200">
        <div className="flex items-center gap-2 min-w-0">
          <FontAwesomeIcon
            icon={faLayerGroup}
            className="text-xs text-indigo-400 dark:text-indigo-400 shrink-0"
          />
          <span className="text-sm truncate">{unit.name}</span>
        </div>

        <div className="flex items-center gap-1 shrink-0">
          <button
            type="button"
            onClick={() => setOpenEditUnitModal(true)}
            className="flex items-center justify-center w-7 h-7 rounded-md text-gray-500 hover:text-indigo-600 hover:bg-indigo-50 dark:text-gray-400 dark:hover:text-indigo-400 dark:hover:bg-indigo-500/10 transition-colors cursor-pointer"
          >
            <FontAwesomeIcon icon={faPen} className="text-xs" />
          </button>
          <button
            type="button"
            onClick={handleDelete}
            className="flex items-center justify-center w-7 h-7 rounded-md text-gray-500 hover:text-red-600 hover:bg-red-50 dark:text-gray-400 dark:hover:text-red-400 dark:hover:bg-red-500/10 transition-colors cursor-pointer"
          >
            <FontAwesomeIcon icon={faTrash} className="text-xs" />
          </button>
        </div>
      </li>

      {openEditUnitModal && (
        <EditUnitModal
          branchId={branchId}
          unitId={unit.id}
          unitName={unit.name}
          onClose={() => setOpenEditUnitModal(false)}
        />
      )}
    </>
  );
}
