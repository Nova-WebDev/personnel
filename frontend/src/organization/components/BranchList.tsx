import { faBuilding, faPen, faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useState } from "react";

import { useTheme } from "../../app/providers/useTheme";
import CollapsibleGroup from "../../base/CollapsibleGroup";
import Modal from "../../base/Modal";
import { confirmDelete } from "../../shared/ui/confirmDelete";
import { useDeleteBranch } from "../hooks/useDeleteBranch";
import { useDeleteUnit } from "../hooks/useDeleteUnit";
import { useUpdateBranch } from "../hooks/useUpdateBranch";
import { useUpdateUnit } from "../hooks/useUpdateUnit";
import type { Branch } from "../types";
import IconAction from "./IconAction";
import RenameForm from "./RenameForm";

type Editing = { kind: "branch" | "unit"; id: string; name: string } | null;

export default function BranchList({ branches }: { branches: Branch[] }) {
  const { theme } = useTheme();
  const [editing, setEditing] = useState<Editing>(null);

  const updateBranch = useUpdateBranch();
  const updateUnit = useUpdateUnit();
  const deleteBranch = useDeleteBranch();
  const deleteUnit = useDeleteUnit();

  const active = editing?.kind === "branch" ? updateBranch : updateUnit;
  const close = () => {
    setEditing(null);
    updateBranch.reset();
    updateUnit.reset();
  };

  const handleRename = (name: string) => {
    if (editing === null) return;
    active.mutate({ id: editing.id, name }, { onSuccess: close });
  };

  const handleDelete = async (
    kind: "branch" | "unit",
    id: string,
    name: string,
  ) => {
    if (!(await confirmDelete(theme === "dark", name))) return;
    if (kind === "branch") deleteBranch.mutate(id);
    else deleteUnit.mutate(id);
  };

  if (branches.length === 0) {
    return (
      <div className="rounded-2xl border border-dashed border-gray-300 p-10 text-center text-gray-500 dark:border-white/15 dark:text-gray-400">
        هنوز سازمانی ثبت نشده است.
      </div>
    );
  }

  return (
    <>
      <div className="space-y-3">
        {branches.map((branch) => (
          <CollapsibleGroup
            key={branch.branch_id}
            variant="card"
            title={branch.branch_name}
            meta={`${branch.units.length.toLocaleString("fa-IR")} واحد`}
            icon={() => <FontAwesomeIcon icon={faBuilding} />}
            actions={[
              {
                render: () => (
                  <IconAction
                    icon={faPen}
                    label="ویرایش"
                    onClick={() =>
                      setEditing({
                        kind: "branch",
                        id: branch.branch_id,
                        name: branch.branch_name,
                      })
                    }
                  />
                ),
              },
              {
                render: () => (
                  <IconAction
                    icon={faTrash}
                    label="حذف"
                    danger
                    onClick={() =>
                      void handleDelete(
                        "branch",
                        branch.branch_id,
                        branch.branch_name,
                      )
                    }
                  />
                ),
              },
            ]}
          >
            {branch.units.length === 0 ? (
              <p className="text-sm text-gray-500 dark:text-gray-400">
                این سازمان واحدی ندارد.
              </p>
            ) : (
              <div className="space-y-2">
                {branch.units.map((unit) => (
                  <CollapsibleGroup
                    key={unit.unit_id}
                    variant="row"
                    title={unit.unit_name}
                    actions={[
                      {
                        render: () => (
                          <IconAction
                            icon={faPen}
                            label="ویرایش"
                            onClick={() =>
                              setEditing({
                                kind: "unit",
                                id: unit.unit_id,
                                name: unit.unit_name,
                              })
                            }
                          />
                        ),
                      },
                      {
                        render: () => (
                          <IconAction
                            icon={faTrash}
                            label="حذف"
                            danger
                            onClick={() =>
                              void handleDelete(
                                "unit",
                                unit.unit_id,
                                unit.unit_name,
                              )
                            }
                          />
                        ),
                      },
                    ]}
                  />
                ))}
              </div>
            )}
          </CollapsibleGroup>
        ))}
      </div>

      <Modal
        open={editing !== null}
        title={editing?.kind === "branch" ? "ویرایش سازمان" : "ویرایش واحد"}
        onClose={close}
      >
        {editing !== null && (
          <RenameForm
            key={editing.id}
            label={editing.kind === "branch" ? "نام سازمان" : "نام واحد"}
            initialName={editing.name}
            isPending={active.isPending}
            error={active.error}
            onSubmit={handleRename}
            onCancel={close}
          />
        )}
      </Modal>
    </>
  );
}
