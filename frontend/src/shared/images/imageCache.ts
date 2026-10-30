import { openDB } from "idb";

const DB_NAME = "image-cache";
const STORE = "images";

const dbPromise = openDB(DB_NAME, 1, {
  upgrade(db) {
    db.createObjectStore(STORE);
  },
});

const urls = new Map<string, string>();
const pending = new Map<string, Promise<string>>();

async function load(key: string, url: string): Promise<string> {
  const db = await dbPromise;
  let blob = (await db.get(STORE, key)) as Blob | undefined;

  if (blob === undefined) {
    const response = await fetch(url, { credentials: "include" });
    if (!response.ok) throw new Error(`image ${response.status}`);
    blob = await response.blob();
    await db.put(STORE, blob, key);
  }

  const objectUrl = URL.createObjectURL(blob);
  urls.set(key, objectUrl);
  return objectUrl;
}

export function getImageUrl(key: string, url: string): Promise<string> {
  const ready = urls.get(key);
  if (ready !== undefined) return Promise.resolve(ready);

  const inflight = pending.get(key);
  if (inflight !== undefined) return inflight;

  const promise = load(key, url).finally(() => pending.delete(key));
  pending.set(key, promise);
  return promise;
}

export async function invalidateImage(key: string): Promise<void> {
  const db = await dbPromise;
  await db.delete(STORE, key);
  const old = urls.get(key);
  if (old !== undefined) URL.revokeObjectURL(old);
  urls.delete(key);
}
