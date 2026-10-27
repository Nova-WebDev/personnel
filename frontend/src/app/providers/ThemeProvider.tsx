import { useState, type ReactNode } from "react";
import { ThemeContext, type Theme } from "./ThemeContext";

const STORAGE_KEY = "theme";

function readInitialTheme(): Theme {
  const stored = localStorage.getItem(STORAGE_KEY);
  const theme: Theme =
    stored === "dark" || stored === "light"
      ? stored
      : window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";

  document.documentElement.classList.toggle("dark", theme === "dark");
  return theme;
}

export default function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(readInitialTheme);

  const changeTheme = (newTheme: Theme) => {
    setTheme(newTheme);
    localStorage.setItem(STORAGE_KEY, newTheme);
    document.documentElement.classList.toggle("dark", newTheme === "dark");
  };

  return (
    <ThemeContext.Provider value={{ theme, changeTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
