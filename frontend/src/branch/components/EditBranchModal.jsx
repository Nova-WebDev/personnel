import { createPortal } from "react-dom";
import { useState } from "react";
import { ModalHeader } from "./ModalHeader";
import { useUpdateBranch } from "../../branch/hooks/useUpdateBranch";
import { useBranchesStore } from "../store/useBranchesStore";

export const EditBranchModal = ({ branchId, branchName, onClose }) => {
  const [name, setName] = useState(branchName || "");
  const [error, setError] = useState("");

  const updateBranchMutation = useUpdateBranch();
  const { updateBranch } = useBranchesStore();

  const validate = () => {
    if (!name.trim()) {
      setError("نام شرکت نمی‌تواند خالی باشد.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    try {
      const response = await updateBranchMutation.mutateAsync({
        branchId,
        name,
      });

      if (response && response.data) {
        updateBranch(branchId, { name: response.data.name });
      } else {
        updateBranch(branchId, { name });
      }

      onClose();
    } catch (err) {
      console.error("Error updating branch:", err);
      setError("خطا در ویرایش شرکت رخ داد.");
    }
  };

  const modal = (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-3 bg-black/40 dark:bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-lg overflow-hidden shadow-xl bg-[#F4F4F5] dark:bg-[#0D1525] border border-gray-300 dark:border-gray-700">
        <ModalHeader title="ویرایش شرکت" onClose={onClose} />
        <div className="p-6 space-y-5" dir="rtl">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="نام شرکت"
            className="w-full px-3 py-2 border rounded-md dark:bg-[#1C2333] dark:text-gray-100"
          />
          {error && <div className="text-sm text-red-600">{error}</div>}
        </div>
        <div className="flex items-center justify-end gap-3 p-4 bg-[#F4F4F5] dark:bg-[#0D1525]">
          <button
            onClick={handleSubmit}
            disabled={updateBranchMutation.isLoading}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 cursor-pointer"
          >
            {updateBranchMutation.isLoading
              ? "در حال ذخیره..."
              : "ذخیره تغییرات"}
          </button>
          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 cursor-pointer"
          >
            بستن
          </button>
        </div>
      </div>
    </div>
  );

  return createPortal(modal, document.body);
};
