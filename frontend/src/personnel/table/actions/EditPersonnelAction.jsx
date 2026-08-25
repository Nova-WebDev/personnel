import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPen } from "@fortawesome/free-solid-svg-icons";

export function EditPersonnelAction({ row, onEdit }) {
  return (
    <button
      onClick={() => onEdit(row)}
      className="flex items-center justify-center w-full gap-2 py-2 pl-5 pr-3 text-sm text-white rounded-md cursor-pointer bg-cyan-600 md:w-auto hover:bg-cyan-700"
    >
      <FontAwesomeIcon icon={faPen} />
      Edite
    </button>
  );
}