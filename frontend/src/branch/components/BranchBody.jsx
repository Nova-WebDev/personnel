import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faChevronDown,
  faBuilding,
  faLayerGroup,
} from "@fortawesome/free-solid-svg-icons";

import { useGetAllBranches } from "../hooks/useGetAllBranches";

function UnitRow({ unit }) {
  return (
    <li className="flex items-center gap-2 p-2.5 rounded-lg bg-white dark:bg-[#1a2742] border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-200">
      <FontAwesomeIcon
        icon={faLayerGroup}
        className="text-xs text-indigo-400 dark:text-indigo-400"
      />
      <span className="text-sm">{unit.name}</span>
    </li>
  );
}

function BranchRow({ branch }) {
  const [open, setOpen] = useState(false);
  const unitCount = branch.units?.length || 0;

  return (
    <li className="rounded-2xl border bg-[#f0f1fb] dark:bg-[#141b30] border-indigo-200 dark:border-[#232f52] transition-all duration-200">
      <div
        className="flex items-center justify-between p-4 cursor-pointer select-none"
        onClick={() => setOpen(!open)}
      >
        <div className="flex items-center gap-3">
          <div className="flex items-center justify-center text-indigo-600 bg-indigo-100 w-9 h-9 rounded-xl dark:bg-indigo-500/10 dark:text-indigo-400">
            <FontAwesomeIcon icon={faBuilding} className="text-sm" />
          </div>
          <div>
            <div className="font-semibold text-gray-800 dark:text-gray-100">
              {branch.name}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400">
              {unitCount} واحد
            </div>
          </div>
        </div>

        <FontAwesomeIcon
          icon={faChevronDown}
          className={`text-gray-500 dark:text-gray-400 transition-transform duration-300 ${
            open ? "rotate-180" : ""
          }`}
        />
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
                <UnitRow key={unit.id} unit={unit} />
              ))}
            </ul>
          )}
        </div>
      )}
    </li>
  );
}

export const BranchBody = () => {
  const [sectionOpen, setSectionOpen] = useState(true);
  const { branches } = useGetAllBranches();
  const branchList = branches || [];

  return (
    <div
      className={`p-4 m-4 mt-8 bg-indigo-100 border border-indigo-100 rounded-2xl md:px-7 dark:bg-indigo-500/10 dark:border-indigo-500/20 ${sectionOpen ? "pb-10" : ""}`}
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
