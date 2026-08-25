import { useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBan, faUnlock, faSpinner } from "@fortawesome/free-solid-svg-icons";
import { useSetPersonnelBlockStatus } from "../../hooks/useSetPersonnelBlockStatus";

export function BlockUnblockAction({ row }) {
  const mutation = useSetPersonnelBlockStatus();
  const [blocked, setBlocked] = useState(row.is_blocked);
  const isLoading = mutation.isPending;

  const handleClick = () => {
    mutation.mutate(
      { personnelUuid: row.uuid, isBlocked: !blocked },
      { onSuccess: () => setBlocked(!blocked) },
    );
  };

  return (
    <button
      disabled={isLoading}
      onClick={handleClick}
      className={`
        flex items-center justify-center gap-2
        w-full md:w-auto
        pl-5 pr-3 py-2 rounded-lg text-sm font-medium
        transition-all duration-200 shadow-sm
        ${
          blocked
            ? "bg-green-600 hover:bg-green-700 text-white cursor-pointer"
            : "bg-red-600 hover:bg-red-700 text-white cursor-pointer"
        }
        ${isLoading ? "opacity-40 cursor-not-allowed" : ""}
      `}
    >
      {isLoading ? (
        <>
          <FontAwesomeIcon icon={faSpinner} spin />
          <span className="animate-pulse">در حال پردازش...</span>
        </>
      ) : (
        <>
          <FontAwesomeIcon icon={blocked ? faUnlock : faBan} />
          <span>{blocked ? "Unblock" : "Block"}</span>
        </>
      )}
    </button>
  );
}