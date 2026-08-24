import { createPortal } from "react-dom";
import { useState } from "react";
import { ModalHeader } from "./ModalHeader";
import { useCreateBranch } from "../../branch/hooks/useCreateBranch";
import { useBranchesStore } from "../store/useBranchesStore";

export const CreateBranchModal = ({ onClose }) => {
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  const createBranchMutation = useCreateBranch();
  const { addBranch } = useBranchesStore();

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
      const response = await createBranchMutation.mutateAsync({ name });
      if (response && response.data) {
        addBranch({ ...response.data, units: [] });
      }
      onClose();
    } catch (err) {
      console.error("Error creating branch:", err);
      setError("خطا در ساخت شرکت رخ داد.");
    }
  };

  const modal = (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-3 bg-black/40 dark:bg-black/50 backdrop-blur-sm">
      <div
        className="
          w-full max-w-lg mx-auto
          rounded-lg overflow-hidden shadow-xl
          bg-[#F4F4F5] dark:bg-[#0D1525]
          border border-gray-300 dark:border-gray-700
        "
      >
        <ModalHeader title="ساخت شرکت" onClose={onClose} />

        <div className="p-6 space-y-5" dir="rtl">
          <div>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="نام شرکت"
              className="w-full px-3 py-2 border rounded-md dark:bg-[#1C2333] dark:text-gray-100"
            />
            {error && (
              <div className="mt-1 text-sm text-red-600 dark:text-red-400">
                {error}
              </div>
            )}
          </div>
        </div>

        <div
          className="
            flex items-center justify-end gap-3 p-4
            bg-[#F4F4F5] dark:bg-[#0D1525] mb-2
          "
        >
          <button
            onClick={handleSubmit}
            disabled={createBranchMutation.isLoading}
            className="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-md cursor-pointer hover:bg-purple-700 dark:bg-purple-700 dark:hover:bg-purple-800"
          >
            {createBranchMutation.isLoading ? "در حال ثبت..." : "ثبت شرکت"}
          </button>

          <button
            onClick={onClose}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-md cursor-pointer hover:bg-gray-300 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600"
          >
            بستن
          </button>
        </div>
      </div>
    </div>
  );

  return createPortal(modal, document.body);
};
