export const ErrorMessage = ({ message }) => {
  if (!message) return null;

  return (
    <div className="text-sm text-red-600 dark:text-red-400">{message}</div>
  );
};