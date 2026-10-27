import { Navigate, type RouteObject } from "react-router-dom";

import PhonePage from "../pages/PhonePage";
import VerifyPage from "../pages/VerifyPage";
import { PublicOnlyRoute } from "./guards";

export const authRoutes: RouteObject[] = [
  {
    path: "auth",
    element: <PublicOnlyRoute />,
    children: [
      { index: true, element: <Navigate to="phone" replace /> },
      { path: "phone", element: <PhonePage /> },
      { path: "verify", element: <VerifyPage /> },
    ],
  },
];
