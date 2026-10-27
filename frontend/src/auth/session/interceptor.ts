import type {
  AxiosError,
  AxiosInstance,
  InternalAxiosRequestConfig,
} from "axios";

import { refreshSession } from "./session";

type RetriableConfig = InternalAxiosRequestConfig & { _retried?: boolean };

export function installRefreshInterceptor(...clients: AxiosInstance[]): void {
  for (const client of clients) {
    client.interceptors.response.use(undefined, async (error: AxiosError) => {
      const config = error.config as RetriableConfig | undefined;
      const isAuthCall = config?.url?.startsWith("/auth/") ?? false;

      if (
        error.response?.status !== 401 ||
        config === undefined ||
        config._retried ||
        isAuthCall
      ) {
        throw error;
      }

      config._retried = true;
      const result = await refreshSession(true);

      if (result !== "ok") throw error;
      return client(config);
    });
  }
}
