import { BranchPage } from "../../branch/pages/BranchPage";
import { PersonnelPage } from "../../personnel/pages/PersonnelPage";
import { Layout } from "../../shared/layout/Layout";

export const appRoutes = [
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        path: "/",
        element: <BranchPage />,
      },
      {
        path: "personnel",
        element: <PersonnelPage />,
      },
    ],
  },
];