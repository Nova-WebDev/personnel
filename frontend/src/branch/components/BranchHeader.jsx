import { useState } from "react";
import { CreateBranchModal } from "./CreateBranchModal";

export const BranchHeader = () => {
  const [openBranchModal, setOpenBranchModal] = useState(false);

  return (
    <div className="flex items-center justify-between w-full mt-5 mb-5 md:mb-2 md:px-7">
      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={() => setOpenBranchModal(true)}
          className="px-4 pt-2 pb-3 text-sm font-medium text-white transition bg-purple-600 rounded-md cursor-pointer hover:bg-purple-700 dark:bg-purple-700 dark:hover:bg-purple-800 whitespace-nowrap"
        >
          ساخت شرکت
        </button>
      </div>

      <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">
        <span className="hidden md:block">شرکت‌ها و واحدها</span>
      </h3>

      {openBranchModal && (
        <CreateBranchModal onClose={() => setOpenBranchModal(false)} />
      )}
    </div>
  );
};
