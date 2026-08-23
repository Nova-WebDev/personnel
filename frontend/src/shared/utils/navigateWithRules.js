export function navigateWithRules(navigate, targetUrl) {
  const currentUrl = window.location.pathname + window.location.search;

  const isAuthRoute =
    currentUrl === "/auth" ||
    currentUrl.startsWith("/auth/");

  const url = new URL(targetUrl, window.location.origin);

  if (isAuthRoute) {
    navigate(url.pathname + url.search);
    return;
  }

  navigate(targetUrl);
}
