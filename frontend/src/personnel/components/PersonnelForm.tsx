import { faCamera, faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  useEffect,
  useRef,
  useState,
  type ChangeEvent,
  type FormEvent,
} from "react";

import { getErrorMessage, normalizeDigits } from "../../auth/utils";
import BranchSelect from "../../organization/components/BranchSelect";
import {
  fieldClass,
  submitClass,
} from "../../organization/components/formStyles";
import { useBranches } from "../../organization/hooks/useBranches";
import fallbackPhoto from "../../shared/assets/photo/profile.png";
import { useCreatePersonnel } from "../hooks/useCreatePersonnel";
import { useUpdatePersonnel } from "../hooks/useUpdatePersonnel";
import type { Personnel } from "../types";
import UnitSelect from "./UnitSelect";

const PHONE_PATTERN = /^09\d{9}$/;
const labelClass = "mb-1.5 block text-sm text-gray-600 dark:text-gray-300";

interface PersonnelFormProps {
  initial?: Personnel;
  onDone: () => void;
}

export default function PersonnelForm({ initial, onDone }: PersonnelFormProps) {
  const { branches } = useBranches();
  const create = useCreatePersonnel();
  const update = useUpdatePersonnel();
  const mutation = initial === undefined ? create : update;

  const [branchId, setBranchId] = useState(initial?.branch_id ?? "");
  const [unitId, setUnitId] = useState(initial?.unit_id ?? "");
  const [phone, setPhone] = useState(initial?.phone ?? "");
  const [firstName, setFirstName] = useState(initial?.first_name ?? "");
  const [lastName, setLastName] = useState(initial?.last_name ?? "");
  const [code, setCode] = useState(initial?.personnel_code ?? "");
  const [photo, setPhoto] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [currentFailed, setCurrentFailed] = useState(false);
  const fileInput = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (photo === null) {
      setPreview(null);
      return;
    }
    const url = URL.createObjectURL(photo);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [photo]);

  const currentPhoto =
    initial !== undefined && initial.photo_path !== null && !currentFailed
      ? `/api/user/photo/${initial.id}`
      : null;
  const shownPhoto = preview ?? currentPhoto ?? fallbackPhoto;

  const units =
    branches.find((branch) => branch.branch_id === branchId)?.units ?? [];
  const canSubmit =
    PHONE_PATTERN.test(phone) &&
    firstName.trim() !== "" &&
    lastName.trim() !== "" &&
    unitId !== "" &&
    (code === "" || code.length === 4) &&
    !mutation.isPending;

  const handleBranch = (id: string) => {
    setBranchId(id);
    setUnitId("");
  };

  const handlePhoto = (event: ChangeEvent<HTMLInputElement>) => {
    setPhoto(event.target.files?.[0] ?? null);
  };

  const clearPhoto = () => {
    setPhoto(null);
    if (fileInput.current !== null) fileInput.current.value = "";
  };

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    if (!canSubmit) return;

    const input = {
      phone,
      first_name: firstName.trim(),
      last_name: lastName.trim(),
      unit_id: unitId,
      personnel_code: code,
      photo,
    };

    if (initial === undefined) create.mutate(input, { onSuccess: onDone });
    else update.mutate({ id: initial.id, input }, { onSuccess: onDone });
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="max-h-[75vh] space-y-4 overflow-y-auto p-4"
    >
      <div className="flex flex-col items-center gap-2">
        <button
          type="button"
          onClick={() => fileInput.current?.click()}
          aria-label="انتخاب عکس"
          className="group relative h-28 w-28 cursor-pointer rounded-full"
        >
          <img
            src={shownPhoto}
            alt=""
            onError={() => setCurrentFailed(true)}
            className="h-full w-full rounded-full object-cover ring-2 ring-teal-500/40 transition group-hover:ring-teal-500"
          />
          <span className="absolute bottom-0 end-0 flex h-9 w-9 items-center justify-center rounded-full bg-teal-600 text-white shadow-md transition group-hover:bg-teal-700">
            <FontAwesomeIcon icon={faCamera} />
          </span>
        </button>

        <input
          ref={fileInput}
          type="file"
          accept="image/png,image/jpeg,image/webp"
          onChange={handlePhoto}
          className="hidden"
        />

        {photo !== null && (
          <button
            type="button"
            onClick={clearPhoto}
            className="flex cursor-pointer items-center gap-1.5 text-xs text-red-600 hover:underline dark:text-red-400"
          >
            <FontAwesomeIcon icon={faXmark} />
            حذف عکس انتخاب‌شده
          </button>
        )}
      </div>

      <div>
        <span className={labelClass}>سازمان</span>
        <BranchSelect
          branches={branches}
          value={branchId}
          onChange={handleBranch}
        />
      </div>

      <div>
        <span className={labelClass}>واحد</span>
        <UnitSelect
          units={units}
          value={unitId}
          disabled={branchId === ""}
          onChange={setUnitId}
        />
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="p-first" className={labelClass}>
            نام
          </label>
          <input
            id="p-first"
            value={firstName}
            onChange={(e) => setFirstName(e.target.value)}
            maxLength={100}
            className={fieldClass}
          />
        </div>
        <div>
          <label htmlFor="p-last" className={labelClass}>
            نام خانوادگی
          </label>
          <input
            id="p-last"
            value={lastName}
            onChange={(e) => setLastName(e.target.value)}
            maxLength={100}
            className={fieldClass}
          />
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <label htmlFor="p-phone" className={labelClass}>
            شماره موبایل
          </label>
          <input
            id="p-phone"
            dir="ltr"
            inputMode="numeric"
            value={phone}
            onChange={(e) =>
              setPhone(normalizeDigits(e.target.value).slice(0, 11))
            }
            placeholder="09123456789"
            className={fieldClass}
          />
        </div>
        <div>
          <label htmlFor="p-code" className={labelClass}>
            کد پرسنلی (اختیاری)
          </label>
          <input
            id="p-code"
            dir="ltr"
            inputMode="numeric"
            value={code}
            onChange={(e) =>
              setCode(normalizeDigits(e.target.value).slice(0, 4))
            }
            placeholder="۴ رقم"
            className={fieldClass}
          />
        </div>
      </div>

      {mutation.error !== null && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(mutation.error, "ثبت پرسنل ناموفق بود.")}
        </p>
      )}

      <button
        type="submit"
        disabled={!canSubmit}
        className={`${submitClass} mt-8 mb-2 w-full flex-none`}
      >
        {mutation.isPending ? "در حال ثبت..." : "ثبت"}
      </button>
    </form>
  );
}
