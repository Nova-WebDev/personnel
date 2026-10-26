# بازبینی مهاجرت Gateway از WebSocket به SSE

گزارش فقط خواندنی است؛ هیچ فایلی تغییر یا اجرا نشده (جز خواندن برای این بررسی).

---

## بخش ۱: انقضای اتصال (سوال اصلی)

**نتیجه: پیاده نشده.** هیچ مکانیزمی برای بستن استریم SSE بر اساس `exp` توکن یا یک سقف زمانی ثابت (مثل ۱ ساعت) وجود ندارد.

### مسیر فعلی اتصال، با خط دقیق

1. احراز هویت فقط یک‌بار، در لحظه‌ی برقراری اتصال، انجام می‌شود:
   - `sse-gateway/auth/dependencies.py:12-15` → `_decoder.decode(access_token)`
   - `sse-gateway/auth/jwt_decoder.py:63-67` (`_check_expiry`) فقط چک می‌کند که در لحظه‌ی حال `exp` گذشته نباشد؛ بعد از آن `exp` دور ریخته می‌شود.
   - `sse-gateway/auth/jwt_decoder.py:28` → `return TokenPayload(public_id=self._read_user_id(payload))` — فقط `public_id` برگردانده می‌شود.
   - `sse-gateway/auth/token_payload.py:3-5` — دیتاکلاس `TokenPayload` فقط فیلد `public_id` دارد؛ جایی برای نگهداری `exp` نیست.
   - `sse-gateway/auth/dependencies.py:17` → `return payload.public_id` — همان رشته‌ی ساده به روتر برمی‌گردد، بدون `exp`.

2. از این نقطه به بعد `exp` در هیچ جای کد sse-gateway وجود ندارد (`grep -rn "exp" sse-gateway` فقط همان `_check_expiry` را برمی‌گرداند).

3. استریم تا ابد باز می‌ماند مگر در یکی از این دو حالت:
   - کلاینت خودش قطع کند → `sse-gateway/routers/sse_router.py:31-36` (`finally: connection_store.remove(stream)`).
   - کل اپ خاموش شود → `sse-gateway/main.py:29` → `connection_store.close_all()` → `sse-gateway/sse/connection_store.py:29-32` → `stream.close()`.
   - این تنها جای کل کدبیس است که `.close()` روی `EventStream` صدا زده می‌شود (تأیید شد با `grep -rn "\.close(" sse-gateway`؛ فقط یک match، همان خط ۳۲ در `connection_store.py`).

4. حلقه‌ی اصلی استریم (`sse-gateway/sse/event_stream.py:37-47`) فقط بین «ایونت رسید» و «تایم‌اوت هارت‌بیت» (`settings.heartbeat_interval`, پیش‌فرض ۱۵ ثانیه) انتخاب می‌کند؛ هیچ شرط `if elapsed >= deadline` در آن نیست.

نکته‌ی جانبی: فرضِ «حداکثر ۱ ساعت» در سوال با تنظیمات واقعی بک‌اند هم‌خوانی ندارد — طول عمر توکن در `backend/auth/infrastructure/signing/token_payload_generator.py:6` پیش‌فرض **۱۵ دقیقه** (`expires_in_seconds: int = 15 * 60`) است، نه یک ساعت.

### چیزی که کم است و پیشنهاد تغییر

کم است:
- انتقال `exp` از decoder تا روتر (الان در مسیر گم می‌شود).
- یک deadline به ازای هر اتصال (`min(exp, created_at + MAX_SESSION_SECONDS)`).
- چک کردن آن deadline در حلقه‌ی `EventStream.__aiter__` و فراخوانی `self.close()`/`return` وقتی زمان برسد.

پیشنهاد (diff نمایشی، اعمال نشده):

```diff
--- a/sse-gateway/auth/token_payload.py
+++ b/sse-gateway/auth/token_payload.py
@@
 class TokenPayload:
     public_id: str
+    exp: int
```

```diff
--- a/sse-gateway/auth/jwt_decoder.py
+++ b/sse-gateway/auth/jwt_decoder.py
@@
-        return TokenPayload(public_id=self._read_user_id(payload))
+        return TokenPayload(public_id=self._read_user_id(payload), exp=payload["exp"])
```

```diff
--- a/sse-gateway/auth/dependencies.py
+++ b/sse-gateway/auth/dependencies.py
@@
-    return payload.public_id
+    return payload
```

```diff
--- a/sse-gateway/settings.py
+++ b/sse-gateway/settings.py
@@
     stream_queue_size: int = 100
     heartbeat_interval: float = 15.0
     client_retry_ms: int = 3000
+    max_session_seconds: int = 3600
```

```diff
--- a/sse-gateway/sse/event_stream.py
+++ b/sse-gateway/sse/event_stream.py
@@
-    def __init__(self, public_id: str):
+    def __init__(self, public_id: str, deadline: float):
         self.public_id = public_id
+        self._deadline = deadline
@@
     async def __aiter__(self) -> AsyncIterator[str]:
         yield format_retry(settings.client_retry_ms)

         while True:
+            remaining = self._deadline - asyncio.get_event_loop().time()
+            if remaining <= 0:
+                return
             try:
-                payload = await asyncio.wait_for(self._queue.get(), settings.heartbeat_interval)
+                payload = await asyncio.wait_for(
+                    self._queue.get(), min(settings.heartbeat_interval, remaining)
+                )
             except TimeoutError:
                 yield format_comment(HEARTBEAT_COMMENT)
                 continue
```

```diff
--- a/sse-gateway/routers/sse_router.py
+++ b/sse-gateway/routers/sse_router.py
@@
-async def stream_events(public_id: str = Depends(get_public_id)) -> StreamingResponse:
-    stream = EventStream(public_id)
+async def stream_events(payload: TokenPayload = Depends(get_public_id)) -> StreamingResponse:
+    deadline = min(payload.exp, time.time() + settings.max_session_seconds)
+    stream = EventStream(payload.public_id, deadline)
```

(نام‌ها و جزئیات دقیق پیاده‌سازی را خودت هماهنگ با سبک پروژه نهایی کن؛ این فقط نمایش شکل تغییر است، نه کد نهایی.)

### بعد از بسته شدن، ۴۰۱ یا reconnect؟

چون سمت سرور چیزی را بر اساس `exp` نمی‌بندد، این سوال در حالت فعلی عملاً مطرح نمی‌شود — استریم باز می‌ماند تا کلاینت قطع کند. اما دو حالت واقعی که الان رخ می‌دهد:

- اگر اتصال به هر دلیل دیگری (قطع شبکه، ری‌استارت گیت‌وی، ری‌استارت nginx) بیفتد و `EventSource` مرورگر خودکار reconnect کند، کوکی `access_token` دوباره فرستاده می‌شود. اگر در همین فاصله توکن واقعاً منقضی شده باشد، درخواست reconnect به‌درستی `401` می‌گیرد (`sse-gateway/auth/dependencies.py:9-15` + `jwt_decoder.py:63-67`). یعنی **اتصال‌های جدید** به‌درستی توسط `exp` فیلتر می‌شوند.
- اما یک استریمی که از قبل باز بوده و توکنش در همین حین منقضی شده، گیت‌وی هیچ‌وقت خودش را نمی‌بندد؛ تا وقتی کلاینت خودش قطع نکند (یا سرور ری‌استارت شود) باز می‌ماند. این دقیقاً همان شکافی است که بخش «چیزی که کم است» توضیح داد.

---

## بخش ۲: چک‌لیست

| # | مورد | وضعیت | فایل و خط |
|---|------|-------|-----------|
| 1 | endpoint، `media_type="text/event-stream"`، `Cache-Control: no-cache`، `X-Accel-Buffering: no` | **OK** | `sse-gateway/routers/sse_router.py:12-16` (هدرها)، `sse-gateway/routers/sse_router.py:19-28` (`@router.get("/events")`, `media_type="text/event-stream"`) |
| 2 | صف محدود برای هر اتصال + بستن اتصال کلاینت کند | **نسبی/مشکل** | صف محدود: `sse-gateway/sse/event_stream.py:13` (`asyncio.Queue(maxsize=settings.stream_queue_size)`). اما کلاینت کند **بسته نمی‌شود** — به‌جایش قدیمی‌ترین فریم صف دراپ می‌شود و اتصال باز می‌ماند: `sse-gateway/sse/event_stream.py:49-54` (`_push`: `self._queue.get_nowait()` سپس شمارش در `self._dropped`). اگر رفتار مطلوب واقعاً «بستن اتصال» است نه «دراپ کردن پیام»، این یک گپ است. |
| 3 | heartbeat با `wait_for` روی `queue.get` (نه busy loop) | **OK** | `sse-gateway/sse/event_stream.py:38-42` (`await asyncio.wait_for(self._queue.get(), settings.heartbeat_interval)` در `except TimeoutError` یک `format_comment` می‌فرستد) |
| 4 | پاک شدن اتصال از `ConnectionStore` هنگام قطع | **OK** | `sse-gateway/routers/sse_router.py:31-36` (`finally: connection_store.remove(stream)`)، و `sse-gateway/sse/connection_store.py:11-18` (`remove` هم از `set` و هم، اگر خالی شود، کل کلید `public_id` را از دیکشنری حذف می‌کند — یعنی memory leak کلید خالی هم ندارد) |
| 5 | ۴۰۱ برای نبود یا نامعتبر بودن کوکی | **OK** | `sse-gateway/auth/dependencies.py:9-10` (نبود کوکی) و `sse-gateway/auth/dependencies.py:12-15` (امضا/فرمت/انقضای نامعتبر از طریق `JWTDecodeError`) |
| 6 | `EventDispatcher` برای `targets=["*"]` و لیست id | **OK** | `sse-gateway/sse/event_dispatcher.py:12-14` (`BROADCAST_TARGET in event.targets` → `connection_store.broadcast`) و `sse-gateway/sse/event_dispatcher.py:16-17` (`for public_id in event.targets: connection_store.send(...)`). سازگار با فرستنده‌ی بک‌اند: `backend/app/events/redis_event_publisher.py:21` (`"targets": targets or ["*"]`) |
| 7 | حذف کامل `PingLoop`/`pong`/کد WebSocket، بدون import یا مرجع مرده | **OK** | فایل‌های `ping_loop.py` و `websocket_handler.py` در `sse-gateway` وجود ندارند (تأیید با لیست کامل فایل‌های پوشه). `grep -rniE "websocket|\bws\b|ping_loop|pong|upgrade"` روی `sse-gateway/`، `docker-compose.yml`، `nginx/nginx.conf` و `backend/` هیچ match ای برنگرداند. |
| 8 | docker-compose.yml و Dockerfile: نام پوشه/سرویس/کانتینر، build context، volume کلید عمومی، healthcheck، depends_on nginx | **OK** | سرویس `sse-gateway` ← `docker-compose.yml:90`؛ `container_name: personnel_sse_gateway` ← `docker-compose.yml:94`؛ `context: ./sse-gateway` ← `docker-compose.yml:92`؛ volume کلید `./sse-gateway/key:/app/key:ro` ← `docker-compose.yml:106`؛ healthcheck ← `docker-compose.yml:107-112`؛ `nginx` منتظر `sse-gateway: condition: service_healthy` ← `docker-compose.yml:128-129` |
| 9 | nginx.conf: location `/events` با `proxy_buffering off`، `proxy_read_timeout` بلند، HTTP/1.1؛ تنظیمات قدیمی Upgrade/Connection حذف‌شده | **OK** | `location /events` ← `nginx/nginx.conf:37-45` شامل `proxy_buffering off;` (خط ۳۹) و `proxy_read_timeout 3600s; proxy_send_timeout 3600s;` (خط‌های ۴۳-۴۴). `proxy_http_version 1.1;` در سطح `http {}` ← `nginx/nginx.conf:9` (برای همه‌ی location ها از جمله `/events` ارث می‌رسد، در خود بلاک `/events` دوباره ست نشده که طبیعی است). هیچ `map $http_upgrade` یا `proxy_set_header Upgrade/Connection $connection_upgrade` در فایل نیست. |
| 10 | `.dockerignore` شامل `*.pem` | **نسبی/مشکل** | هیچ پترن `*.pem` در فایل نیست. آن‌چه هست خط `key` در `sse-gateway/.dockerignore:12` که کل پوشه‌ی `key/` (محل تنها فایل `.pem` فعلی) را از build context کنار می‌گذارد. عملاً امروز کار می‌کند، ولی این حفاظت به نام یک پوشه‌ی خاص وابسته است نه به پسوند فایل؛ اگر یک `.pem` جای دیگری در پوشه قرار بگیرد (مثلاً کنار `main.py`)، دیگر مستثنی نمی‌شود. |

---

## بخش ۳: خلاصه (اولویت‌بندی‌شده)

1. **بستن اتصال بر اساس انقضای توکن (بخش ۱) — بیشترین اولویت.**
   مشکل: `exp` در `jwt_decoder.py:28` / `token_payload.py` دور ریخته می‌شود؛ هیچ deadline‌ای روی عمر استریم اعمال نمی‌شود؛ تنها راه بسته‌شدن، قطع خودِ کلاینت یا خاموشی کامل سرویس است.
   پیشنهاد کوتاه: `exp` را تا `TokenPayload` و از آن تا `sse_router.py` منتقل کن، یک `deadline = min(exp, now + MAX_SESSION)` بساز و در حلقه‌ی `EventStream.__aiter__` (`event_stream.py:37`) هر بار قبل از `wait_for` چک کن که از deadline نگذشته باشی؛ اگر گذشته، `return` کن تا استریم با یک HTTP response عادی (نه قطع ناگهانی) بسته شود و کلاینت مجبور شود با کوکی تازه دوباره وصل شود.

2. **رفتار صف پر برای کلاینت کند با انتظار مطرح‌شده در کار همخوان نیست.**
   مشکل: `event_stream.py:49-54` به‌جای قطع کلاینت کند، قدیمی‌ترین پیام را بی‌صدا دور می‌ریزد (lossy، نه fail-fast).
   پیشنهاد کوتاه: اگر رفتار مطلوب واقعاً قطع اتصال است، در `_push` وقتی `self._queue.full()` به‌جای drop یک‌طرفه، `self.close()` صدا بزن (یا حداقل این رفتار عمدی را در یک کامنت/تصمیم مکتوب جایی ثبت کن تا «کم‌کاری» به نظر نرسد).

3. **`.dockerignore` بر اساس نام پوشه نه پسوند فایل، کلید را مستثنی می‌کند.**
   مشکل: نبود پترن صریح `*.pem` در `sse-gateway/.dockerignore`.
   پیشنهاد کوتاه: یک خط `*.pem` به `sse-gateway/.dockerignore` اضافه شود تا مستقل از نام پوشه، هر فایل کلید در build context باقی نماند.

هیچ مشکل دیگری در چک‌لیست بخش ۲ پیدا نشد؛ موارد ۱، ۳، ۴، ۵، ۶، ۷، ۸، ۹ همگی با ارجاع دقیق فایل/خط تأیید شدند.
