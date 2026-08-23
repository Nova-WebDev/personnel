import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Cookies from "js-cookie";

import Loader from "../base/loading/Loader";
import { decodeJWT } from "../shared/utils/jwt";
import { useUserStore } from "../auth/store/useUserStore";
import { useRefreshToken } from "../auth/hooks/useRefreshToken";
import { refreshTokens } from "../auth/actions/refreshTokens";
import { redirectWithRules } from "../shared/utils/redirectWithRules";

export default function AppProviders({ children }) {
  const navigate = useNavigate();
  const location = useLocation();

  const { mutate: refreshMutate } = useRefreshToken();
  const [isReady, setIsReady] = useState(false);

  const navigateRef = useRef(navigate);
  const locationRef = useRef(location);

  useEffect(() => {
    navigateRef.current = navigate;
    locationRef.current = location;
  }, [navigate, location]);

  useEffect(() => {
    const check = () => {
      const path = locationRef.current.pathname;
      const refresh_token = localStorage.getItem("refresh_token");
      const access_token = Cookies.get("access_token");

      if (!refresh_token) {
        if (!path.startsWith("/auth")) {
          redirectWithRules("/auth/phone");
        }
        return;
      }

      if (!access_token) {
        refreshTokens(refreshMutate, refresh_token);
        return;
      }

      let decoded;
      try {
        decoded = decodeJWT(access_token);
      } catch {
        decoded = null;
      }

      if (!decoded) {
        refreshTokens(refreshMutate, refresh_token);
        return;
      }

      const userState = useUserStore.getState();
      if (userState.exp === null) {
        useUserStore.getState().setUserFromToken(decoded);
      }

      const now = Math.floor(Date.now() / 1000);
      const remaining = decoded.exp - now;

      if (remaining < 300) {
        refreshTokens(refreshMutate, refresh_token);
        return;
      }
    };

    check();
    const interval = setInterval(check, 60000);
    return () => clearInterval(interval);
  }, [refreshMutate]);

  const path = location.pathname;

  useEffect(() => {
    Promise.resolve().then(() => {
      setIsReady(true);
    });
  }, [path]);

  useEffect(() => {
    if (!isReady) return;

    const refresh_token = localStorage.getItem("refresh_token");

    if (refresh_token) {
      if (path.startsWith("/auth")) {
        navigateRef.current("/");
      }
    } else {
      if (!path.startsWith("/auth")) {
        redirectWithRules("/auth/phone");
      }
    }
  }, [isReady, path]);

  if (!isReady) {
    return <Loader />;
  }

  return children;
}
