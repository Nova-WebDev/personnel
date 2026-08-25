import { useEffect, useState } from "react";
import { useRef } from "react";

import defaultProfile from "../../../shared/assets/photo/profile.png";

export const PhotoField = ({ file, onChange, initialPhotoUrl }) => {
  const inputRef = useRef(null);
  const [previewUrl, setPreviewUrl] = useState(null);

  useEffect(() => {
    if (!file) {
      setPreviewUrl(null);
      return;
    }

    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    return () => URL.revokeObjectURL(url);
  }, [file]);

  const displaySrc = previewUrl || initialPhotoUrl || defaultProfile;

  return (
    <div className="flex flex-col items-center gap-2">
      <img
        src={displaySrc}
        alt="پیش‌نمایش عکس پرسنل"
        onClick={() => inputRef.current?.click()}
        className="object-cover w-24 h-24 border-2 border-indigo-200 rounded-full cursor-pointer dark:border-indigo-500/30"
      />

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={(e) => onChange(e.target.files?.[0] || null)}
        className="hidden"
      />
    </div>
  );
};