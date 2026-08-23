import Cookies from "js-cookie";
import { decodeJWT } from "../../shared/utils/jwt";
import { useUserStore } from "../store/useUserStore";

export function refreshTokens(refreshMutate, refresh_token) {
  if (!refresh_token) return;

  refreshMutate(
    { refresh_token },
    {
      onSuccess: (res) => {
        const { access_token, refresh_token: newRefresh } = res.data;
        localStorage.setItem("refresh_token", newRefresh);
        Cookies.set("access_token", access_token, {
          secure: true,
          sameSite: "strict",
        });
        const decoded = decodeJWT(access_token);
        if (decoded) {
          useUserStore.getState().setUserFromToken(decoded);
        }
      },
      onError: (error) => {
        if (
          error.response?.status === 401 &&
          error.response?.data?.detail === "Invalid refresh token"
        ) {
          localStorage.removeItem("refresh_token");
          Cookies.remove("access_token");
        }
      },
    },
  );
}
