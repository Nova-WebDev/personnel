import { BranchPage } from "../../branch/pages/BranchPage";
import { PersonnelPage } from "../../personnel/pages/PersonnelPage";
import { PersonnelCardPage } from "../../personnel/pages/PersonnelCardPage";
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
  {
    path: "card/:uuid",
    element: <PersonnelCardPage />,
  },
];