import type { IconDefinition } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

interface IconActionProps {
  icon: IconDefinition;
  label: string;
  danger?: boolean;
  onClick: () => void;
}

export default function IconAction({
  icon,
  label,
  danger = false,
  onClick,
}: IconActionProps) {
  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={label}
      title={label}
      className={`flex h-8 w-8 cursor-pointer items-center justify-center rounded-lg text-sm transition ${
        danger
          ? "text-gray-500 hover:bg-red-50 hover:text-red-600 dark:text-gray-400 dark:hover:bg-red-500/10 dark:hover:text-red-400"
          : "text-gray-500 hover:bg-teal-50 hover:text-teal-700 dark:text-gray-400 dark:hover:bg-teal-400/10 dark:hover:text-teal-300"
      }`}
    >
      <FontAwesomeIcon icon={icon} />
    </button>
  );
}
