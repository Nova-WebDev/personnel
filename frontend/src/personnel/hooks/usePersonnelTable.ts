import { useState } from "react";

import type { TableState } from "../../base/Table";
import type { Personnel } from "../types";

const SORT_KEYS: Record<string, (user: Personnel) => string> = {
  name: (user) => `${user.first_name} ${user.last_name}`,
  phone: (user) => user.phone,
  personnel_code: (user) => user.personnel_code ?? "",
  unit_name: (user) => user.unit_name ?? "",
  branch_name: (user) => user.branch_name ?? "",
  rfid: (user) => (user.rfid_card_id === null ? "0" : "1"),
};

function matches(user: Personnel, query: string): boolean {
  const haystack = [
    user.first_name,
    user.last_name,
    user.phone,
    user.personnel_code ?? "",
    user.unit_name ?? "",
    user.branch_name ?? "",
  ]
    .join(" ")
    .toLowerCase();
  return haystack.includes(query);
}

export function usePersonnelTable(users: Personnel[]): TableState<Personnel> {
  const [page, setPage] = useState(1);
  const [limit, setLimit] = useState(20);
  const [orderBy, setOrderBy] = useState<string | undefined>(undefined);
  const [deorder, setDeorder] = useState(false);
  const [search, setSearch] = useState("");

  const query = search.trim().toLowerCase();
  const filtered =
    query === "" ? users : users.filter((user) => matches(user, query));

  const sorter = orderBy === undefined ? undefined : SORT_KEYS[orderBy];
  const sorted =
    sorter === undefined
      ? filtered
      : [...filtered].sort(
          (a, b) =>
            sorter(a).localeCompare(sorter(b), "fa") * (deorder ? -1 : 1),
        );

  const lastPage = Math.max(1, Math.ceil(sorted.length / limit));
  const currentPage = Math.min(page, lastPage);
  const data = sorted.slice((currentPage - 1) * limit, currentPage * limit);

  return {
    data,
    total: sorted.length,
    page: currentPage,
    limit,
    orderBy,
    deorder,
    search,
    setPage,
    setLimit,
    setOrderBy,
    setDeorder,
    setSearch,
  };
}
