import AuthLayout from "../layouts/AuthLayout";
import PhonePage from "../ui/PhonePage";
import VerifyPage from "../ui/VerifyPage";

export const authRoutes = [
  {
    path: "/auth",
    element: <AuthLayout />,
    children: [
      {
        index: true,
        element: <PhonePage />,
      },
      {
        path: "phone",
        element: <PhonePage />,
      },
      {
        path: "verify",
        element: <VerifyPage />,
      },
    ],
  },
];
