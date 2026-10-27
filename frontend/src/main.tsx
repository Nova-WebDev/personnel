import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { RouterProvider } from "react-router-dom";

import { installRefreshInterceptor } from "./auth/session";
import api from "./shared/lib/axios";
import axiosMultipart from "./shared/lib/axiosMultipart";
import "./index.css";
import router from "./app/router";

installRefreshInterceptor(api, axiosMultipart);

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
);
