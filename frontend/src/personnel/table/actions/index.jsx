import { EditPersonnelAction } from "./EditPersonnelAction";
import { QrCodeAction } from "./QrCodeAction";
import { BlockUnblockAction } from "./BlockUnblockAction";

export const personnelActions = ({ onEdit }) => [
  {
    label: () => "عملیات",
    render: (row) => (
      <div className="flex flex-col w-full gap-3 md:flex-row md:px-0">
        <EditPersonnelAction row={row} onEdit={onEdit} />
        <QrCodeAction row={row} />
        <BlockUnblockAction row={row} />
      </div>
    ),
  },
];