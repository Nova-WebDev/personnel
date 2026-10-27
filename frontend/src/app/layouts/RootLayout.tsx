import { QueryClientProvider } from "@tanstack/react-query";
import { Outlet } from "react-router-dom";

import AppProviders from "../AppProviders";
import ThemeProvider from "../providers/ThemeProvider";
import { queryClient } from "../queryClient";

export default function RootLayout() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider>
        <AppProviders>
          <Outlet />
        </AppProviders>
      </ThemeProvider>
    </QueryClientProvider>
  );
}
