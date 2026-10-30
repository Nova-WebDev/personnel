import { useEffect, useState } from "react";

import { getImageUrl } from "./imageCache";

export function useCachedImage(
  key: string | null,
  url: string | null,
): string | null {
  const [state, setState] = useState<{ key: string; src: string } | null>(null);

  useEffect(() => {
    if (key === null || url === null) return;
    let active = true;
    getImageUrl(key, url)
      .then((src) => {
        if (active) setState({ key, src });
      })
      .catch(() => {
        if (active) setState(null);
      });
    return () => {
      active = false;
    };
  }, [key, url]);

  return state !== null && state.key === key ? state.src : null;
}
