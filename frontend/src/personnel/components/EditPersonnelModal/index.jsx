import { createPortal } from "react-dom";
import { useState } from "react";

import { ModalHeader } from "../../../branch/components/ModalHeader";
import { useUpdatePersonnel } from "../../hooks/useUpdatePersonnel";
import { getPersonnelPhotoUrl } from "../../api/personnelApi";

import { PhotoField } from "../CreatePersonnelModal/PhotoField";
import { FirstNameField } from "../CreatePersonnelModal/FirstNameField";
import { LastNameField } from "../CreatePersonnelModal/LastNameField";
import { PersonnelIdField } from "../CreatePersonnelModal/PersonnelIdField";
import { BranchField } from "../CreatePersonnelModal/BranchField";
import { UnitField } from "../CreatePersonnelModal/UnitField";
import { PositionField } from "../CreatePersonnelModal/PositionField";
import { ErrorMessage } from "../CreatePersonnelModal/ErrorMessage";

export const EditPersonnelModal = ({ onClose, branchesQuery, personnel }) => {
  const [file, setFile] = useState(null);
  const [firstName, setFirstName] = useState(personnel.first_name);
  const [lastName, setLastName] = useState(personnel.last_name);
  const [personnelId, setPersonnelId] = useState(personnel.personnel_id);
  const [branchId, setBranchId] = useState(String(personnel.branch_id ?? ""));
  const [unitId, setUnitId] = useState(String(personnel.unit_id ?? ""));
  const [position, setPosition] = useState(String(personnel.position ?? ""));
  const [error, setError] = useState("");

  const updatePersonnelMutation = useUpdatePersonnel();

  const branchList = branchesQuery?.branches || [];
  const selectedBranch = branchList.find((b) => b.id === Number(branchId));
  const unitList = selectedBranch?.units || [];

  const initialFileId = personnel.photo_path
    ? personnel.photo_path.split("/").pop()
    : null;
  const initialPhotoUrl = initialFileId
    ? getPersonnelPhotoUrl(initialFileId)
    : null;

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
    await updatePersonnelMutation.mutateAsync({
      personnelUuid: personnel.uuid,
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
    console.error("Error updating personnel:", err);
    setError("خطا در ویرایش پرسنل رخ داد.");
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
        <div className="overflow-hidden rounded-t-lg">
          <ModalHeader title="ویرایش پرسنل" onClose={onClose} />
        </div>

        <div className="p-6 space-y-4" dir="rtl">
          <PhotoField
            file={file}
            onChange={setFile}
            initialPhotoUrl={initialPhotoUrl}
          />
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
            flex items-center justify-end gap-3 p-4 rounded-b-lg overflow-hidden
            bg-[#F4F4F5] dark:bg-[#0D1525] mb-2
          "
        >
          <button
            onClick={handleSubmit}
            disabled={updatePersonnelMutation.isLoading}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md cursor-pointer hover:bg-blue-700 dark:bg-blue-700 dark:hover:bg-blue-800"
          >
            {updatePersonnelMutation.isLoading
              ? "در حال ثبت..."
              : "ذخیره تغییرات"}
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