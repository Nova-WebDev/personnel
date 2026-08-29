import { NavLink } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSitemap, faIdCard, faRightFromBracket } from "@fortawesome/free-solid-svg-icons";
import Separator from "../../base/ui/Separator";
import { useLogout } from "../../auth/hooks/useLogout";

export const SidebarMenu = () => {
  const logoutMutation = useLogout();

  const menu = [
    {
      to: "/",
      label: "شعبه‌ها و واحدها",
      icon: faSitemap,
    },
    {
      to: "/personnel",
      label: "پرسنل",
      icon: faIdCard,
    },
  ];

  const handleLogout = () => {
    const refresh_token = localStorage.getItem("refresh_token");
    logoutMutation.mutate({ refresh_token });
  };

  return (
    <div className="w-full h-full bg-[#F4F4F5] dark:bg-[#111C2E] border-l border-gray-300 dark:border-gray-700 pt-6 px-3 flex flex-col">

      <div className="pr-1 mb-5 mr-2 text-lg font-bold tracking-wide text-gray-700 dark:text-gray-300">
        منوی اصلی
      </div>

      <Separator width="90%" />

      <div className="flex flex-col gap-2 mt-3">
        {menu.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              `
              flex items-center gap-3 px-4 py-3 rounded-lg cursor-pointer transition
              text-gray-800 dark:text-gray-200
              hover:bg-gray-200 dark:hover:bg-gray-700
              ${isActive ? "bg-indigo-200 text-indigo-900 hover:bg-indigo-200 dark:bg-gray-700 dark:text-indigo-300 font-bold" : ""}
              `
            }
          >
            <FontAwesomeIcon icon={item.icon} className="w-5 h-5" />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </div>

      <div className="flex-1" />

      <div className="mb-6">
        <Separator width="90%" />
        <button
          onClick={handleLogout}
          disabled={logoutMutation.isPending}
          className="flex items-center w-full gap-3 px-4 py-3 mt-3 text-red-600 transition rounded-lg cursor-pointer dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-500/10 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <FontAwesomeIcon icon={faRightFromBracket} className="w-5 h-5" />
          <span>{logoutMutation.isPending ? "در حال خروج..." : "خروج از حساب"}</span>
        </button>
      </div>
    </div>
  );
};