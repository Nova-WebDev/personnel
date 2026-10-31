import { faIdCard } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useRef, useState, type KeyboardEvent } from "react";

import { getErrorMessage } from "../../auth/utils";
import { cancelClass } from "../../organization/components/formStyles";
import { useSetRfid } from "../hooks/useSetRfid";
import type { Personnel } from "../types";

const RFID_LENGTH = 10;
const RFID_PATTERN = /^[0-9A-F]{10}$/;

interface RfidFormProps {
  user: Personnel;
  onDone: () => void;
}

export default function RfidForm({ user, onDone }: RfidFormProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [invalid, setInvalid] = useState(false);
  const setRfid = useSetRfid();

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key !== "Enter") return;
    event.preventDefault();

    const raw = event.currentTarget.value.trim().toUpperCase();
    event.currentTarget.value = "";
    const rfid = raw.slice(-RFID_LENGTH);

    if (!RFID_PATTERN.test(rfid)) {
      setInvalid(true);
      return;
    }

    setInvalid(false);
    setRfid.mutate({ id: user.id, rfid }, { onSuccess: onDone });
  };

  return (
    <div className="space-y-5 p-6 text-center">
      <input
        ref={inputRef}
        autoFocus
        autoComplete="off"
        onKeyDown={handleKeyDown}
        onBlur={() => inputRef.current?.focus()}
        className="pointer-events-none absolute h-0 w-0 opacity-0"
        aria-label="RFID"
      />

      <div className="mx-auto flex h-20 w-20 animate-float-soft items-center justify-center rounded-full bg-teal-500/10 text-3xl text-teal-600 dark:text-teal-300">
        <FontAwesomeIcon icon={faIdCard} />
      </div>

      <div>
        <p className="font-semibold text-gray-800 dark:text-gray-100">
          {user.first_name} {user.last_name}
        </p>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
          {setRfid.isPending ? "در حال ثبت..." : "کارت را اسکن کنید"}
        </p>
      </div>

      {invalid && (
        <p className="text-sm text-red-600 dark:text-red-400">
          کارت نامعتبر است، دوباره اسکن کنید.
        </p>
      )}
      {setRfid.error !== null && (
        <p className="text-sm text-red-600 dark:text-red-400">
          {getErrorMessage(setRfid.error, "ثبت کارت ناموفق بود.")}
        </p>
      )}

      <button
        type="button"
        onClick={onDone}
        className={`${cancelClass} w-full flex-none`}
      >
        انصراف
      </button>
    </div>
  );
}
