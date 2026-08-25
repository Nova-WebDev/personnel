import { getPersonnelPhotoUrl } from "../../api/personnelApi";
import defaultProfile from "../../../shared/assets/photo/profile.png";

export function PhotoCell({ photoPath }) {
  const fileId = photoPath ? photoPath.split("/").pop() : null;
  const src = fileId ? getPersonnelPhotoUrl(fileId) : defaultProfile;

  return (
    <div className="flex pt-2 pr-2 md:justify-start md:pr-0 md:pt-0">
      <img
        src={src}
        alt="عکس پرسنل"
        className="object-cover border border-gray-200 rounded-full md:w-10 md:h-10 w-15 h-15 dark:border-gray-700"
      />
    </div>
  );
}