import { useState } from "react";

import { CreatePersonnelModal } from "./CreatePersonnelModal";

export const PersonnelHeader = ({ branchesQuery }) => {
  const [openPersonnelModal, setOpenPersonnelModal] = useState(false);

  return (
    <div className="flex items-center justify-between w-full mt-5 mb-5 md:mb-2 md:px-4">
      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={() => setOpenPersonnelModal(true)}
          className="px-4 pt-2 pb-3 text-sm font-medium text-white transition bg-blue-600 rounded-md cursor-pointer hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 whitespace-nowrap"
        >
          ساخت پرسنل
        </button>
      </div>

      <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">
        <span className="hidden md:block">پرسنل</span>
      </h3>

      {openPersonnelModal && (
        <CreatePersonnelModal
          onClose={() => setOpenPersonnelModal(false)}
          branchesQuery={branchesQuery}
        />
      )}
    </div>
  );
};