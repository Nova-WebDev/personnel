import { useState } from "react";

import Table from "../../base/ui/Table";
import { personnelColumns } from "../table/columns";
import { personnelActions } from "../table/actions";
import { usePersonnelTableData } from "../hooks/usePersonnelTableData";
import { EditPersonnelModal } from "./EditPersonnelModal";

export const PersonnelBody = ({ branchesQuery }) => {
  const table = usePersonnelTableData({
    page: 1,
    limit: 20,
    orderBy: "created_at",
    deorder: true,
    search: "",
  });

  const [openEdit, setOpenEdit] = useState(false);
  const [selectedPersonnel, setSelectedPersonnel] = useState(null);

  return (
    <div>
      <Table
        columns={personnelColumns}
        actions={personnelActions({
          onEdit: (row) => {
            setSelectedPersonnel(row);
            setOpenEdit(true);
          },
        })}
        table={table}
      />

      {openEdit && selectedPersonnel && (
        <EditPersonnelModal
          personnel={selectedPersonnel}
          branchesQuery={branchesQuery}
          table={table}
          onClose={() => setOpenEdit(false)}
        />
      )}
    </div>
  );
};