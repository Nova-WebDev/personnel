export const PersonnelIdField = ({ value, onChange }) => {
  return (
    <input
      type="text"
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder="شماره پرسنلی"
      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md dark:bg-[#1C2333] dark:text-gray-100 focus:outline-none focus:border-indigo-400 dark:focus:border-indigo-500 focus:ring-1 focus:ring-indigo-400 dark:focus:ring-indigo-500"
    />
  );
};