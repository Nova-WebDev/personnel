import { ClipLoader } from "react-spinners";

export default function Loader() {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-cyan-50 dark:bg-[#06141b]">
      <ClipLoader color="#14b8a6" size={48} />
    </div>
  );
}
