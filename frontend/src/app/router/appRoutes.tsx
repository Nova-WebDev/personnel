import type { RouteObject } from "react-router-dom";

import { ProtectedRoute } from "../../auth/router/guards";

export const appRoutes: RouteObject[] = [
  {
    element: <ProtectedRoute />,
    children: [{ index: true, element: <div className="p-6">Home</div> }],
  },
];
