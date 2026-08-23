import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBars, faMoon, faSun } from "@fortawesome/free-solid-svg-icons";
import { useTheme } from "../../shared/hooks/useTheme";
import { useState } from "react";


export const Header = ({ isOpen, setIsOpen }) => {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    setTheme(theme === "dark" ? "light" : "dark");
  };

  return (
    <>
      <div className="flex items-center justify-between px-6 py-4  border-b border-[#231F6B]  dark:border-gray-700">
        <div className="flex items-center gap-3">
          <h1 className="hidden text-lg font-bold text-white md:block dark:text-gray-200">
            Hooman Holding
          </h1>

          <button
            className="text-xl text-white md:hidden dark:text-gray-200"
            onClick={() => setIsOpen(!isOpen)}
          >
            <FontAwesomeIcon icon={faBars} className="w-6 h-6" />
          </button>
        </div>

        <div className="flex items-center gap-5">
          <button
            onClick={toggleTheme}
            className="flex items-center justify-center w-10 h-10 text-white transition rounded-full cursor-pointer bg-white/20 dark:bg-gray-700 dark:text-gray-200 hover:bg-white/30 dark:hover:bg-gray-600"
          >
            <FontAwesomeIcon
              icon={theme === "dark" ? faSun : faMoon}
              className="w-5 h-5"
            />
          </button>     
        </div>
      </div>

    </>
  );
};