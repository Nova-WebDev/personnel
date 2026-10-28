import type { RouteObject } from "react-router-dom";

import AccessPage from "../../access/pages/AccessPage";
import { ProtectedRoute } from "../../auth/router/guards";
import CyclePage from "../../cycle/pages/CyclePage";
import DashboardPage from "../../dashboard/pages/DashboardPage";
import HomePage from "../../home/pages/HomePage";
import MealsManagePage from "../../meals/pages/MealsManagePage";
import MealsPage from "../../meals/pages/MealsPage";
import OrganizationPage from "../../organization/pages/OrganizationPage";
import PersonnelPage from "../../personnel/pages/PersonnelPage";
import TimePolicyPage from "../../policy/pages/TimePolicyPage";
import ProfilePage from "../../profile/pages/ProfilePage";
import RedeemPage from "../../redeem/pages/RedeemPage";
import DayReportPage from "../../reports/pages/DayReportPage";
import { RoleRoute } from "../../user/guards/RoleRoute";
import MainLayout from "../layouts/MainLayout";

export const appRoutes: RouteObject[] = [
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <MainLayout />,
        children: [
          { index: true, element: <HomePage /> },
          { path: "meals", element: <MealsPage /> },
          { path: "profile", element: <ProfilePage /> },
          {
            element: <RoleRoute allow={["kitchen"]} />,
            children: [
              { path: "redeem", element: <RedeemPage /> },
              { path: "reports/day", element: <DayReportPage /> },
              { path: "manage/meals", element: <MealsManagePage /> },
            ],
          },
          {
            element: <RoleRoute allow={["hr_manager"]} />,
            children: [{ path: "personnel", element: <PersonnelPage /> }],
          },
          {
            element: <RoleRoute allow={["admin"]} />,
            children: [
              { path: "admin/dashboard", element: <DashboardPage /> },
              { path: "admin/organization", element: <OrganizationPage /> },
              { path: "admin/access", element: <AccessPage /> },
              { path: "admin/time-policy", element: <TimePolicyPage /> },
              { path: "admin/meal-cycle", element: <CyclePage /> },
            ],
          },
        ],
      },
    ],
  },
];
