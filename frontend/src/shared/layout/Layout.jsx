import { Outlet, useLocation } from "react-router-dom";
import { Sidebar } from "../components/Sidebar";
import { Header } from "../components/Header";
import { useState, useEffect } from "react";

export const Layout = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    Promise.resolve().then(() => {
      setIsOpen(false);
    });
  }, [location.pathname]);

  return (
    <div dir="rtl" className="flex h-screen overflow-hidden">
      <Sidebar isOpen={isOpen} setIsOpen={setIsOpen} />

      <div className="flex flex-col flex-1 h-full min-w-0">
        <div className="shrink-0 bg-[#312E81] dark:bg-[#0D1525]">
          <Header isOpen={isOpen} setIsOpen={setIsOpen} />
        </div>

        <div className="flex-1 overflow-y-auto bg-[#F4F4F5] dark:bg-[#111C2E]">
          <Outlet />
        </div>
      </div>
    </div>
  );
};