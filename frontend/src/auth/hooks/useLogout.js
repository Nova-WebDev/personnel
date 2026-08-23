import { useMutation } from "@tanstack/react-query";
import { logout } from "../../auth/api/authApi";
import Cookies from "js-cookie";
import { useUserStore } from "../../auth/store/useUserStore";
import { useProfileStore } from "../../user/store/profileStore";
import { useNavigate } from "react-router-dom";

export function useLogout() {
  const clearAuth = useUserStore((s) => s.clearUser);
  const clearProfile = useProfileStore((s) => s.clearProfile);
  const navigate = useNavigate();

  return useMutation({
    mutationFn: ({ refresh_token }) => logout(refresh_token),
    onSuccess: () => {
      localStorage.removeItem("refresh_token");
      Cookies.remove("access_token");
      clearAuth();
      clearProfile();
      navigate("/auth/phone");
    },
    onError: () => {
      localStorage.removeItem("refresh_token");
      Cookies.remove("access_token");
      clearAuth();
      clearProfile();
      navigate("/auth/phone");
    },
  });
}
