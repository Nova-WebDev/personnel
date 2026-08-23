import { BranchPage } from "../../branch/pages/BranchPage";
import { HomePage } from "../../home/pages/HomePage";
import { PersonnelPage } from "../../personnel/pages/PersonnelPage";
import { Layout } from "../../shared/layout/Layout";

export const appRoutes = [
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "branches",
        element: <BranchPage />,
      },
      {
        path: "personnel",
        element: <PersonnelPage />,
      },
      {
        path: "/",
        element: <HomePage />,
      },
    ],
  },
];