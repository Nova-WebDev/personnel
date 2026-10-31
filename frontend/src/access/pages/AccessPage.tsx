import { faLock, faPlus } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

import Loader from "../../base/loading/Loader";
import Modal from "../../base/Modal";
import { useBranches } from "../../organization/hooks/useBranches";
import { usePersonnel } from "../../personnel/hooks/usePersonnel";
import AddPermissionForm from "../components/AddPermissionForm";
import HolderRow from "../components/HolderRow";
import RoleTabs from "../components/RoleTabs";
import { usePermissions } from "../hooks/usePermissions";
import { ROLES, type RoleKey } from "../types";

export default function AccessPage() {
  const [selected, setSelected] = useState<RoleKey>("ADMIN");
  const [adding, setAdding] = useState(false);

  const { permissions, isLoading, isError } = usePermissions();
  const personnel = usePersonnel();
  useBranches();

  const role = ROLES.find((item) => item.key === selected) ?? ROLES[0];
  const counts = Object.fromEntries(
    ROLES.map((item) => [
      item.key,
      permissions.filter(
        (permission) => permission.level.toUpperCase() === item.key,
      ).length,
    ]),
  ) as Record<RoleKey, number>;
  const holders = permissions.filter(
    (permission) => permission.level.toUpperCase() === selected,
  );
  const loading = isLoading || personnel.isLoading;

  return (
    <div className="space-y-6">
      <RoleTabs selected={selected} counts={counts} onSelect={setSelected} />

      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
          {role.label}
        </h2>
        {role.locked ? (
          <span className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
            <FontAwesomeIcon icon={faLock} />
            نقش ادمین قابل تغییر نیست
          </span>
        ) : (
          <button
            type="button"
            onClick={() => setAdding(true)}
            className="flex h-10 cursor-pointer items-center gap-2 rounded-lg bg-teal-600 px-4 text-sm font-medium text-white transition hover:bg-teal-700"
          >
            <FontAwesomeIcon icon={faPlus} />
            افزودن
          </button>
        )}
      </div>

      {loading && <Loader fullscreen={false} size={12} />}
      {isError && (
        <p className="text-red-600 dark:text-red-400">
          دریافت دسترسی‌ها ناموفق بود.
        </p>
      )}

      {!loading && !isError && holders.length === 0 && (
        <div className="rounded-2xl border border-dashed border-slate-300 p-10 text-center text-slate-500 dark:border-white/15 dark:text-slate-400">
          کسی این نقش را ندارد.
        </div>
      )}

      {!loading && !isError && holders.length > 0 && (
        <ul className="grid gap-3 md:grid-cols-2">
          {holders.map((permission) => (
            <HolderRow
              key={permission.permission_id}
              permission={permission}
              scoped={role.scoped}
              locked={role.locked}
            />
          ))}
        </ul>
      )}

      <Modal
        open={adding}
        title={`افزودن ${role.label}`}
        onClose={() => setAdding(false)}
      >
        {adding && (
          <AddPermissionForm role={role} onDone={() => setAdding(false)} />
        )}
      </Modal>
    </div>
  );
}
