export default function Separator({
  width = "2rem",
  height = "1px",
  className = "",
}) {
  return (
    <div
      style={{ width, height }}
      className={`
        mx-auto my-0.5 bg-gray-400 dark:bg-gray-600
        ${className}
      `}
    />
  );
}
