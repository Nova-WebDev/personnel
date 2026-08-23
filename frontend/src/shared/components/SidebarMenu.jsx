import { NavLink } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faSitemap, faIdCard } from "@fortawesome/free-solid-svg-icons";
import Separator from "../../base/ui/Separator";

export const SidebarMenu = () => {
  const menu = [
    {
      to: "/branches",
      label: "شعبه‌ها و واحدها",
      icon: faSitemap,
    },
    {
      to: "/personnel",
      label: "پرسنل",
      icon: faIdCard,
    },
  ];

  return (
    <div className="w-full h-full bg-[#F4F4F5] dark:bg-[#111C2E] border-l border-gray-300 dark:border-gray-700 pt-6 px-3">

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
    </div>
  );
};