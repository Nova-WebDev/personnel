interface DefaultMealImageProps {
  className?: string;
}

export default function DefaultMealImage({
  className = "",
}: DefaultMealImageProps) {
  return (
    <svg
      viewBox="0 0 64 64"
      role="img"
      aria-label="بدون عکس"
      className={`bg-teal-100 text-teal-500 dark:bg-[#12384a] dark:text-teal-300 ${className}`}
    >
      <g fill="currentColor">
        <rect x="18" y="14" width="3" height="14" rx="1.5" />
        <rect x="24" y="14" width="3" height="14" rx="1.5" />
        <rect x="30" y="14" width="3" height="14" rx="1.5" />
        <path d="M18 26h15v2a7.5 7.5 0 0 1-15 0z" />
        <rect x="23.5" y="32" width="4" height="20" rx="2" />
        <ellipse cx="44" cy="22" rx="6" ry="9" />
        <rect x="42" y="30" width="4" height="22" rx="2" />
      </g>
    </svg>
  );
}
