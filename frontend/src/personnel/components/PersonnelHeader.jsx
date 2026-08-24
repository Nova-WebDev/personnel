import React from "react";

export const PersonnelHeader = () => {
  return (
    <div className="flex items-center justify-between w-full mt-2">
      <div className="flex flex-wrap items-center gap-2">
        <button
          className="px-4 pt-2 pb-3 text-sm font-medium text-white transition bg-blue-600 rounded-md cursor-pointer hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800 whitespace-nowrap"
        >
          ساخت پرسنل
        </button>
      </div>

      <h3 className="text-xl font-bold text-gray-800 dark:text-gray-100">
        <span className="hidden md:block">پرسنل</span>
      </h3>
    </div>
  );
};
