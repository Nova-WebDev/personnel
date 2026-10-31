import { faCheck, faXmark } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

import type { TableColumn } from "../../base/Table";
import Avatar from "../../shared/ui/Avatar";
import type { PersonnelView } from "../types";

export const personnelColumns: TableColumn<PersonnelView>[] = [
  {
    label: "نام",
    orderBy: "name",
    render: (user) => (
      <div className="flex w-full items-center justify-start gap-3 text-start">
        <Avatar
          id={user.id}
          photoPath={user.photo_path}
          className="h-9 w-9 shrink-0"
        />
        <span className="font-medium">
          {user.first_name} {user.last_name}
        </span>
      </div>
    ),
  },
  {
    label: "موبایل",
    orderBy: "phone",
    render: (user) => <span dir="ltr">{user.phone}</span>,
  },
  {
    label: "کد پرسنلی",
    orderBy: "personnel_code",
    render: (user) => user.personnel_code ?? "—",
  },
  {
    label: "واحد",
    orderBy: "unit_name",
    render: (user) => user.unit_name ?? "—",
  },
  {
    label: "سازمان",
    orderBy: "branch_name",
    render: (user) => user.branch_name ?? "—",
  },
  {
    label: "کارت",
    orderBy: "rfid",
    render: (user) =>
      user.rfid_card_id === null ? (
        <FontAwesomeIcon icon={faXmark} className="text-red-500" />
      ) : (
        <FontAwesomeIcon
          icon={faCheck}
          className="text-teal-600 dark:text-teal-300"
        />
      ),
  },
];
