import { PhotoCell } from "./cells/PhotoCell";
import { BranchNameCell } from "./cells/BranchNameCell";
import { UnitNameCell } from "./cells/UnitNameCell";
import { PositionCell } from "./cells/PositionCell";

export const personnelColumns = [
  {
    label: "عکس",
    render: (row) => <PhotoCell photoPath={row.photo_path} />,
  },
  {
    label: "نام",
    orderBy: "first_name",
    render: (row) => row.first_name,
  },
  {
    label: "نام‌خانوادگی",
    orderBy: "last_name",
    render: (row) => row.last_name,
  },
  {
    label: "شرکت",
    orderBy: "branch_id",
    render: (row) => <BranchNameCell branchId={row.branch_id} />,
  },
  {
    label: "واحد",
    orderBy: "unit_id",
    render: (row) => (
      <UnitNameCell branchId={row.branch_id} unitId={row.unit_id} />
    ),
  },
  {
    label: "سمت",
    orderBy: "position",
    render: (row) => <PositionCell position={row.position} />,
  },
];