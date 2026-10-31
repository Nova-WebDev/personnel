import {
  faBan,
  faIdCard,
  faLockOpen,
  faMagnifyingGlass,
  faPen,
  faPlus,
  faQrcode,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

import { usePermissions } from "../../access/hooks/usePermissions";
import Loader from "../../base/loading/Loader";
import Modal from "../../base/Modal";
import Table, { type TableAction } from "../../base/Table";
import { useMeStore } from "../../user/store/useMeStore";
import ActionButton from "../components/ActionButton";
import PersonnelForm from "../components/PersonnelForm";
import { personnelColumns } from "../components/personnelColumns";
import QrModalContent from "../components/QrModalContent";
import RfidCheck from "../components/RfidCheck";
import RfidForm from "../components/RfidForm";
import { usePersonnel } from "../hooks/usePersonnel";
import { usePersonnelTable } from "../hooks/usePersonnelTable";
import { useSetBlocked } from "../hooks/useSetBlocked";
import type { PersonnelView } from "../types";

type ActiveModal =
  | { kind: "create" }
  | { kind: "edit"; user: PersonnelView }
  | { kind: "rfid"; user: PersonnelView }
  | { kind: "qr"; user: PersonnelView }
  | { kind: "check" }
  | null;

const titles = {
  create: "افزودن پرسنل",
  edit: "ویرایش پرسنل",
  rfid: "ثبت کارت RFID",
  qr: "کد QR",
  check: "بررسی کارت",
} as const;

export default function PersonnelPage() {
  const [active, setActive] = useState<ActiveModal>(null);
  const { users, isLoading, isError } = usePersonnel();
  const { permissions } = usePermissions();
  const table = usePersonnelTable(users);
  const setBlocked = useSetBlocked();
  const myId = useMeStore((state) => state.me?.id ?? null);

  const adminIds = new Set(
    permissions
      .filter((item) => item.level.toUpperCase() === "ADMIN")
      .map((item) => item.user_id),
  );

  const close = () => setActive(null);

  const actions: TableAction<PersonnelView>[] = [
    {
      label: () => "Edit",
      render: (user) => (
        <ActionButton
          icon={faPen}
          onClick={() => setActive({ kind: "edit", user })}
        >
          Edit
        </ActionButton>
      ),
    },
    {
      label: () => "Add RFID",
      render: (user) => (
        <ActionButton
          icon={faIdCard}
          onClick={() => setActive({ kind: "rfid", user })}
        >
          Add RFID
        </ActionButton>
      ),
    },
    {
      label: () => "QR",
      render: (user) => (
        <ActionButton
          icon={faQrcode}
          onClick={() => setActive({ kind: "qr", user })}
        >
          QR
        </ActionButton>
      ),
    },
    {
      label: () => "Block",
      render: (user) => {
        const isSelf = user.id === myId;
        const isAdmin = adminIds.has(user.id);
        const reason = isSelf
          ? "نمی‌توانید خودتان را مسدود کنید"
          : isAdmin
            ? "ادمین قابل مسدود شدن نیست"
            : undefined;

        return (
          <ActionButton
            tone={user.is_blocked ? "success" : "danger"}
            icon={user.is_blocked ? faLockOpen : faBan}
            disabled={isSelf || isAdmin}
            title={reason}
            onClick={() =>
              setBlocked.mutate({ id: user.id, isBlocked: !user.is_blocked })
            }
          >
            {user.is_blocked ? "Unblock" : "Block"}
          </ActionButton>
        );
      },
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={() => setActive({ kind: "create" })}
          className="flex h-11 cursor-pointer items-center gap-2 rounded-lg bg-teal-600 px-5 text-sm font-medium text-white transition hover:bg-teal-700"
        >
          <FontAwesomeIcon icon={faPlus} />
          افزودن پرسنل
        </button>
        <button
          type="button"
          onClick={() => setActive({ kind: "check" })}
          className="flex h-11 cursor-pointer items-center gap-2 rounded-lg border border-teal-600 px-5 text-sm font-medium text-teal-700 transition hover:bg-teal-50 dark:border-teal-400/60 dark:text-teal-300 dark:hover:bg-teal-400/10"
        >
          <FontAwesomeIcon icon={faMagnifyingGlass} />
          بررسی کارت
        </button>
        {!isLoading && !isError && (
          <span className="text-sm text-slate-500 dark:text-slate-400">
            {users.length.toLocaleString("fa-IR")} نفر
          </span>
        )}
      </div>

      {isLoading && <Loader fullscreen={false} size={12} />}
      {isError && (
        <p className="text-red-600 dark:text-red-400">
          دریافت پرسنل ناموفق بود.
        </p>
      )}
      {!isLoading && !isError && (
        <Table columns={personnelColumns} actions={actions} table={table} />
      )}

      <Modal
        open={active !== null}
        title={active === null ? "" : titles[active.kind]}
        onClose={close}
      >
        {active?.kind === "create" && <PersonnelForm onDone={close} />}
        {active?.kind === "edit" && (
          <PersonnelForm
            key={active.user.id}
            initial={active.user}
            onDone={close}
          />
        )}
        {active?.kind === "rfid" && (
          <RfidForm key={active.user.id} user={active.user} onDone={close} />
        )}
        {active?.kind === "qr" && (
          <QrModalContent key={active.user.id} user={active.user} />
        )}
        {active?.kind === "check" && <RfidCheck />}
      </Modal>
    </div>
  );
}
