import { PulseLoader } from "react-spinners";

import { useTheme } from "../../app/providers/useTheme";

interface LoaderProps {
  fullscreen?: boolean;
  size?: number;
}

export default function Loader({ fullscreen = true, size = 14 }: LoaderProps) {
  const { theme } = useTheme();
  const color = theme === "dark" ? "#5eead4" : "#0d9488";

  const wrapper = fullscreen
    ? "fixed inset-0 z-50 flex items-center justify-center bg-slate-100 dark:bg-[#06141b]"
    : "flex items-center justify-center py-16";

  return (
    <div className={wrapper} role="status" aria-label="در حال بارگذاری">
      <PulseLoader color={color} size={size} speedMultiplier={0.8} />
    </div>
  );
}
