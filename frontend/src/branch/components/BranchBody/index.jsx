import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown } from "@fortawesome/free-solid-svg-icons";

import { useGetAllBranches } from "../../hooks/useGetAllBranches";
import { BranchRow } from "./BranchRow";

export const BranchBody = () => {
  const [sectionOpen, setSectionOpen] = useState(true);
  const { branches } = useGetAllBranches();
  const branchList = branches || [];

  return (
    <div
      className={`p-4 md:m-4 mt-7 md:mt-8 bg-indigo-100 border border-indigo-100 rounded-2xl md:px-7 dark:bg-indigo-500/10 dark:border-indigo-500/20 ${sectionOpen ? "pb-10" : ""}`}
    >
      <div
        className="flex items-center justify-between mb-4 cursor-pointer select-none"
        onClick={() => setSectionOpen(!sectionOpen)}
      >
        <h3 className="text-lg font-bold text-gray-800 dark:text-gray-100">
          شرکت‌ها
        </h3>
        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-gray-500 dark:text-gray-400 transition-transform duration-300 ${
            sectionOpen ? "rotate-180" : ""
          }`}
        />
      </div>

      {sectionOpen && (
        <ul className="space-y-3">
          {branchList.map((branch) => (
            <BranchRow key={branch.id} branch={branch} />
          ))}
        </ul>
      )}
    </div>
  );
};
