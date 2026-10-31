import { faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import { useTheme } from "../../app/providers/useTheme";
import { usePersonnelStore } from "../../personnel/store/usePersonnelStore";
import Avatar from "../../shared/ui/Avatar";
import { confirmDelete } from "../../shared/ui/confirmDelete";
import { useRemovePermission } from "../hooks/usePermissionMutations";
import type { Permission } from "../types";

interface HolderRowProps {
  permission: Permission;
  scoped: boolean;
  locked: boolean;
}

export default function HolderRow({
  permission,
  scoped,
  locked,
}: HolderRowProps) {
  const { theme } = useTheme();
  const photoPath = usePersonnelStore(
    (state) => state.users[permission.user_id]?.photo_path ?? null,
  );
  const remove = useRemovePermission();

  const name = `${permission.first_name} ${permission.last_name}`.trim();
  const place = [permission.unit_name, permission.branch_name]
    .filter(Boolean)
    .join(" · ");

  const handleRemove = async () => {
    if (await confirmDelete(theme === "dark", `دسترسی ${name}`))
      remove.mutate(permission);
  };

  return (
    <li className="flex items-center gap-3 rounded-xl border border-slate-200 bg-white p-3 dark:border-white/10 dark:bg-[#0c242f]">
      <Avatar
        id={permission.user_id}
        photoPath={photoPath}
        className="h-10 w-10 shrink-0"
      />
      <div className="min-w-0 flex-1">
        <p className="truncate font-medium text-slate-900 dark:text-slate-100">
          {name}
        </p>
        {scoped && (
          <p className="truncate text-xs text-slate-500 dark:text-slate-400">
            {place || "واحد حذف شده"}
          </p>
        )}
      </div>
      {!locked && (
        <button
          type="button"
          onClick={() => void handleRemove()}
          disabled={remove.isPending}
          aria-label="حذف دسترسی"
          className="flex h-9 w-9 cursor-pointer items-center justify-center rounded-lg text-slate-500 transition hover:bg-red-50 hover:text-red-600 disabled:opacity-60 dark:text-slate-400 dark:hover:bg-red-500/10 dark:hover:text-red-400"
        >
          <FontAwesomeIcon icon={faTrash} />
        </button>
      )}
    </li>
  );
}
