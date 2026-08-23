export function redirectWithRules(targetUrl) {
  const currentUrl = window.location.pathname + window.location.search;

  const isAuthRoute =
    currentUrl === "/auth" ||
    currentUrl.startsWith("/auth/");

  const url = new URL(targetUrl, window.location.origin);

  if (isAuthRoute) {
    window.location.assign(url.toString());
    return;
  }

  window.location.assign(targetUrl);
}
