import { createPortal } from "react-dom";
import { useState } from "react";
import { ModalHeader } from "./ModalHeader";
import { useCreateUnit } from "../../branch/hooks/useCreateUnit";
import { useBranchesStore } from "../store/useBranchesStore";

export const CreateUnitModal = ({ branchId, onClose }) => {
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  const createUnitMutation = useCreateUnit();
  const { addUnit } = useBranchesStore();

  const validate = () => {
    if (!name.trim()) {
      setError("نام واحد نمی‌تواند خالی باشد.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    try {
      const response = await createUnitMutation.mutateAsync({ name, branchId });

      if (response && response.data) {
        addUnit(branchId, response.data);
      } else {
        addUnit(branchId, { id: Date.now(), name });
      }

      onClose();
    } catch (err) {
      console.error("Error creating unit:", err);
      setError("خطا در ساخت واحد رخ داد.");
    }
  };

  const modal = (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-3 bg-black/40 dark:bg-black/50 backdrop-blur-sm">
      <div className="w-full max-w-md rounded-lg overflow-hidden shadow-xl bg-[#F4F4F5] dark:bg-[#0D1525] border border-gray-300 dark:border-gray-700">
        <ModalHeader title="افزودن واحد جدید" onClose={onClose} />
        <div className="p-6 space-y-5" dir="rtl">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="نام واحد"
            className="w-full px-3 py-2 border rounded-md dark:bg-[#1C2333] dark:text-gray-100"
          />
          {error && <div className="text-sm text-red-600">{error}</div>}
        </div>
        <div className="flex items-center justify-end gap-3 p-4 bg-[#F4F4F5] dark:bg-[#0D1525]">
          <button
            onClick={handleSubmit}
            disabled={createUnitMutation.isLoading}
            className="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 dark:bg-green-700 dark:hover:bg-green-800 cursor-pointer"
          >
            {createUnitMutation.isLoading ? "در حال ثبت..." : "ثبت واحد"}
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
