import { SidebarMenu } from "./SidebarMenu";

export const Sidebar = ({ isOpen, setIsOpen }) => {
  return (
    <>
      <div className="hidden h-screen bg-white md:block w-72 min-w-72 dark:bg-gray-800">
        <SidebarMenu />
      </div>

      <div
        className={`fixed h-screen inset-y-0 right-0 w-72 min-w-72 bg-white dark:bg-gray-800 transform transition-transform duration-300 ease-in-out z-50 md:hidden ${
          isOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <SidebarMenu />
      </div>

      {isOpen && (
        <div
          className="fixed inset-0 z-40 bg-black/30 backdrop-blur-sm md:hidden"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  );
};
