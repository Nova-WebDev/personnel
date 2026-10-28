import { useState } from "react";

import fallback from "../assets/photo/profile.png";

interface AvatarProps {
  id: string;
  photoPath: string | null;
  className?: string;
}

export default function Avatar({ id, photoPath, className = "" }: AvatarProps) {
  const [failed, setFailed] = useState(false);
  const src =
    photoPath !== null && !failed ? `/api/user/photo/${id}` : fallback;

  return (
    <img
      src={src}
      alt=""
      onError={() => setFailed(true)}
      className={`rounded-full object-cover ring-2 ring-teal-500/30 ${className}`}
    />
  );
}
