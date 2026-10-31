import {
  faCircleCheck,
  faCircleXmark,
  faIdCard,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useRef, useState, type KeyboardEvent } from "react";

import Avatar from "../../shared/ui/Avatar";
import { isUnitAllowed } from "../../user/permissions";
import { useMeStore } from "../../user/store/useMeStore";
import { usePersonnelStore } from "../store/usePersonnelStore";
import type { Personnel } from "../types";

const RFID_LENGTH = 10;
const RFID_PATTERN = /^[0-9A-F]{10}$/;

type Result =
  | { kind: "found"; user: Personnel }
  | { kind: "missing" }
  | { kind: "invalid" }
  | null;

export default function RfidCheck() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [result, setResult] = useState<Result>(null);

  const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key !== "Enter") return;
    event.preventDefault();

    const raw = event.currentTarget.value.trim().toUpperCase();
    event.currentTarget.value = "";
    const rfid = raw.slice(-RFID_LENGTH);

    if (!RFID_PATTERN.test(rfid)) {
      setResult({ kind: "invalid" });
      return;
    }

    const { users, rfidIndex } = usePersonnelStore.getState();
    const { hrUnitIds } = useMeStore.getState();
    const userId = rfidIndex[rfid];
    const user = userId === undefined ? undefined : users[userId];

    if (user === undefined || !isUnitAllowed(hrUnitIds, user.unit_id)) {
      setResult({ kind: "missing" });
      return;
    }
    setResult({ kind: "found", user });
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

      {result === null && (
        <>
          <div className="mx-auto flex h-20 w-20 animate-float-soft items-center justify-center rounded-full bg-teal-500/10 text-3xl text-teal-600 dark:text-teal-300">
            <FontAwesomeIcon icon={faIdCard} />
          </div>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            کارت را اسکن کنید
          </p>
        </>
      )}

      {result?.kind === "invalid" && (
        <p className="text-sm text-red-600 dark:text-red-400">
          کارت نامعتبر است، دوباره اسکن کنید.
        </p>
      )}

      {result?.kind === "missing" && (
        <div className="space-y-2">
          <FontAwesomeIcon
            icon={faCircleXmark}
            className="text-5xl text-red-500"
          />
          <p className="font-semibold text-gray-800 dark:text-gray-100">
            این کارت در لیست شما وجود ندارد
          </p>
        </div>
      )}

      {result?.kind === "found" && (
        <div className="space-y-3">
          <FontAwesomeIcon
            icon={faCircleCheck}
            className="text-5xl text-emerald-500"
          />
          <p className="font-semibold text-emerald-600 dark:text-emerald-400">
            این کارت وجود دارد
          </p>
          <div className="flex items-center justify-center gap-3 rounded-xl bg-slate-100 p-3 dark:bg-white/5">
            <Avatar
              id={result.user.id}
              photoPath={result.user.photo_path}
              className="h-12 w-12 shrink-0"
            />
            <div className="text-start">
              <p className="font-medium text-gray-800 dark:text-gray-100">
                {result.user.first_name} {result.user.last_name}
              </p>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                {[result.user.unit_name, result.user.branch_name]
                  .filter(Boolean)
                  .join(" · ")}
              </p>
            </div>
          </div>
        </div>
      )}

      {result !== null && (
        <p className="text-xs text-gray-400 dark:text-gray-500">
          برای بررسی کارت بعدی، آن را اسکن کنید.
        </p>
      )}
    </div>
  );
}
