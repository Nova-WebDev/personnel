import { useState } from "react";
import { useGetPersonnelPaginated } from "./useGetPersonnelPaginated";

export function usePersonnelTableData({
  page: initialPage = 1,
  limit: initialLimit = 20,
  orderBy: initialOrderBy = "created_at",
  deorder: initialDeorder = true,
  search: initialSearch = "",
} = {}) {
  const [page, setPage] = useState(initialPage);
  const [limit, setLimit] = useState(initialLimit);
  const [orderBy, setOrderBy] = useState(initialOrderBy);
  const [deorder, setDeorder] = useState(initialDeorder);
  const [search, setSearch] = useState(initialSearch);

  const { data, isLoading, error } = useGetPersonnelPaginated({
    page,
    limit,
    search: search || null,
    orderBy,
    descending: deorder,
  });

  return {
    data: data?.data?.personnel || [],
    total: data?.data?.total_count || 0,
    page,
    limit,
    orderBy,
    deorder,
    search,
    setPage,
    setLimit,
    setOrderBy,
    setDeorder,
    setSearch,
    isLoading,
    error,
  };
}