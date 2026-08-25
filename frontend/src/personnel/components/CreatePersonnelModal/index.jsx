import { createPortal } from "react-dom";
import { useState } from "react";

import { ModalHeader } from "../../../branch/components/ModalHeader";
import { useCreatePersonnel } from "../../hooks/useCreatePersonnel";

import { PhotoField } from "./PhotoField";
import { FirstNameField } from "./FirstNameField";
import { LastNameField } from "./LastNameField";
import { PersonnelIdField } from "./PersonnelIdField";
import { BranchField } from "./BranchField";
import { UnitField } from "./UnitField";
import { PositionField } from "./PositionField";
import { ErrorMessage } from "./ErrorMessage";

export const CreatePersonnelModal = ({ onClose, branchesQuery }) => {
  const [file, setFile] = useState(null);
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [personnelId, setPersonnelId] = useState("");
  const [branchId, setBranchId] = useState("");
  const [unitId, setUnitId] = useState("");
  const [position, setPosition] = useState("");
  const [error, setError] = useState("");

  const createPersonnelMutation = useCreatePersonnel();

  const branchList = branchesQuery?.branches || [];
  const selectedBranch = branchList.find((b) => b.id === Number(branchId));
  const unitList = selectedBranch?.units || [];

  const validate = () => {
    if (!firstName.trim()) {
      setError("نام نمی‌تواند خالی باشد.");
      return false;
    }
    if (!lastName.trim()) {
      setError("نام‌خانوادگی نمی‌تواند خالی باشد.");
      return false;
    }
    if (!personnelId.trim()) {
      setError("شماره پرسنلی نمی‌تواند خالی باشد.");
      return false;
    }
    if (!branchId) {
      setError("انتخاب شرکت الزامی است.");
      return false;
    }
    setError("");
    return true;
  };

  const handleSubmit = async () => {
  if (!validate()) return;

  try {
    await createPersonnelMutation.mutateAsync({
      file,
      firstName,
      lastName,
      personnelId,
      branchId: Number(branchId),
      unitId: unitId ? Number(unitId) : null,
      position: position ? Number(position) : null,
    });
    window.location.reload();
  } catch (err) {
    console.error("Error creating personnel:", err);
    setError("خطا در ساخت پرسنل رخ داد.");
  }
};

  const handleBranchChange = (value) => {
    setBranchId(value);
    setUnitId("");
  };

  const modal = (
    <div className="fixed inset-0 z-50 flex items-center justify-center px-3 bg-black/40 dark:bg-black/50 backdrop-blur-sm">
      <div
        className="
          w-full max-w-lg mx-auto
          rounded-lg shadow-xl
          bg-[#F4F4F5] dark:bg-[#0D1525]
          border border-gray-300 dark:border-gray-700
        "
      >
        <ModalHeader title="ساخت پرسنل" onClose={onClose} />

        <div className="p-6 space-y-4" dir="rtl">
          <PhotoField file={file} onChange={setFile} />
          <FirstNameField value={firstName} onChange={setFirstName} />
          <LastNameField value={lastName} onChange={setLastName} />
          <PersonnelIdField value={personnelId} onChange={setPersonnelId} />
          <BranchField
            value={branchId}
            onChange={handleBranchChange}
            branchList={branchList}
          />
          <UnitField
            value={unitId}
            onChange={setUnitId}
            unitList={unitList}
            disabled={!branchId}
          />
          <PositionField value={position} onChange={setPosition} />
          <ErrorMessage message={error} />
        </div>

        <div
          className="
            flex items-center justify-end gap-3 p-4
            bg-[#F4F4F5] dark:bg-[#0D1525] mb-2
          "
        >
          <button
            onClick={handleSubmit}
            disabled={createPersonnelMutation.isLoading}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md cursor-pointer hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800"
          >
            {createPersonnelMutation.isLoading ? "در حال ثبت..." : "ثبت پرسنل"}
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