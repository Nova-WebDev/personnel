import fallback from "../assets/photo/profile.png";
import { useCachedImage } from "../images/useCachedImage";

interface AvatarProps {
  id: string;
  photoPath: string | null;
  className?: string;
}

export default function Avatar({ id, photoPath, className = "" }: AvatarProps) {
  const hasPhoto = photoPath !== null;
  const src = useCachedImage(
    hasPhoto ? `profile:${id}` : null,
    hasPhoto ? `/api/user/photo/${id}` : null,
  );

  return (
    <img
      src={src ?? fallback}
      alt=""
      className={`rounded-full object-cover ring-2 ring-teal-500/30 ${className}`}
    />
  );
}
