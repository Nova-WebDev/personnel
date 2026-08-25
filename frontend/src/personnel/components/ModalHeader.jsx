import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes } from "@fortawesome/free-solid-svg-icons";

export const ModalHeader = ({ title, onClose }) => {
  return (
    <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
      <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">
        {title}
      </h2>

      <button
        onClick={onClose}
        className="text-gray-500 cursor-pointer dark:text-gray-300 hover:text-red-600 dark:hover:text-red-500"
      >
        <FontAwesomeIcon icon={faTimes} className="w-5 h-5" />
      </button>
    </div>
  );
};