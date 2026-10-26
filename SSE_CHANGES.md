# تغییرات اعمال‌شده روی sse-gateway

سه تغییر زیر، طبق درخواست، در `sse-gateway` اعمال شد. چیزی commit نشده.

---

## ۱. انقضای استریم بر اساس `exp`

### فایل‌های تغییریافته

- `sse-gateway/auth/token_payload.py` — فیلد `exp: int` به دیتاکلاس `TokenPayload` اضافه شد.
- `sse-gateway/auth/jwt_decoder.py:28` — `JWTDecoder.decode` حالا `exp=payload["exp"]` را هم در `TokenPayload` برمی‌گرداند (`_check_expiry` قبل از این خط تضمین کرده که `exp` از نوع `int` است).
- `sse-gateway/auth/dependencies.py` — تابع از `get_public_id` (که فقط رشته برمی‌گرداند) به `get_token_payload` تغییر کرد و کل `TokenPayload` (شامل `exp`) را برمی‌گرداند، نه فقط `public_id`.
- `sse-gateway/routers/sse_router.py` — `stream_events` حالا `Depends(get_token_payload)` می‌گیرد و `EventStream(payload.public_id, payload.exp)` را با `deadline=payload.exp` می‌سازد.
- `sse-gateway/sse/event_stream.py` — `EventStream.__init__` حالا `deadline: int` (epoch ثانیه، همان `exp`) می‌پذیرد. در `__aiter__`، قبل از هر `wait_for`:
  ```python
  remaining = self.deadline - time.time()
  if remaining <= 0:
      return
  ```
  و تایم‌اوت صف هم `min(settings.heartbeat_interval, remaining)` است تا استریم دقیقاً روی مرز `deadline` بیدار شود، نه بعدش. مقایسه با `time.time()` (ساعت epoch سیستم) انجام می‌شود، نه `loop.time()` (که monotonic و بدون مرجع تقویمی است) — همان‌طور که خواسته شده بود.

`max_session_seconds` در کدبیس اصلاً اضافه نشده بود (در بازبینی قبلی فقط به‌عنوان پیشنهاد diff در `SSE_REVIEW.md` نوشته شده بود، هیچ‌وقت در `settings.py` واقعی پیاده نشد)، بنابراین چیزی برای حذف در `settings.py` وجود نداشت؛ `settings.py` دست‌نخورده ماند.

### تست (اجرا شد، نه فقط نوشته شد)

یک درخواست SSE واقعی روی ASGI باز شد با توکنی که `exp = now + 1` دارد:

```
PASS  stream opens 200 before expiry
PASS  registered in connection_store
PASS  stream task completes on its own near exp (no client disconnect needed)
PASS  connection_store cleaned up after exp-driven close
PASS  no error frame, just retry/heartbeat frames before close
```

یعنی بدون اینکه کلاینت قطع کند، حدود ۱ ثانیه بعد از باز شدن، خودِ تسکِ ASGI تمام شد و رکورد اتصال از `ConnectionStore` حذف شد.

---

## ۲. بسته شدن استریم وقتی صف پر است

### فایل تغییریافته

`sse-gateway/sse/event_stream.py`:
- `_push` دیگر وقتی صف پر است پیام قدیمی را drop نمی‌کند؛ به‌جایش `self.close()` را صدا می‌زند و برمی‌گردد.
- `close()` حالا سنتینل پایان (`None`) را از طریق متد جدید `_force_push` وارد صف می‌کند؛ `_force_push` اگر صف پر باشد یک آیتم را با `get_nowait()` خارج می‌کند تا جای سنتینل باز شود (این یکی مورد، نه برای پیام‌های معمولی، فقط برای تضمین رسیدن سیگنال پایان).
- شمارنده‌ی `dropped`/`_dropped` حذف شد چون دیگر هیچ‌جا «drop» رخ نمی‌دهد و چیزی برای شمارش نبود؛ هیچ ارجاع دیگری به آن در کدبیس نبود (چک شد با grep قبل از حذف).

### تست (اجرا شد)

یک `EventStream` مستقیم با `maxsize=3` ساخته شد (از `STREAM_QUEUE_SIZE=3`):

```
PASS  queue accepts up to its maxsize without closing
PASS  stream closes itself once the queue is full
PASS  queue still bounded at maxsize after forced sentinel
PASS  no event named 'after-close' leaked once closed
PASS  stream generator terminates after draining the backlog + sentinel
```

یعنی تا ۳ پیام صف پر می‌شود بدون بسته‌شدن؛ پیام چهارم باعث `close()` می‌شود؛ بعد از `close()` پیام‌های جدید دیگر پذیرفته نمی‌شوند؛ و مصرف‌کننده همان ۳ پیامِ باقی‌مانده در صف را می‌گیرد و بعد با سنتینل تمام می‌شود (نه قطع ناگهانی وسط پیام).

---

## ۳. `.dockerignore`

`sse-gateway/.dockerignore` یک خط `*.pem` گرفت (بعد از خط `key`، قبل از `.dockerignore`). فایل کامل فعلی:

```
.venv
venv
env
.git
.gitignore
.idea
__pycache__
*.pyc
*.pyo
.env
logs
key
*.pem
.dockerignore
Dockerfile
README.md
```

---

## رگرسیون (اجرا شد)

برای اطمینان از این‌که مسیرهای قبلی نشکسته‌اند:

```
PASS  no cookie -> 401
PASS  valid token -> 200
PASS  retry frame first
PASS  normal delivery still works end-to-end
PASS  client disconnect still cleans up
```

---

## تغییر رفتار قابل‌مشاهده برای کلاینت

- اگر توکن هنوز معتبر است، چیزی فرق نمی‌کند.
- وقتی `exp` برسد، سرور خودش استریم را با یک پایان تمیز HTTP می‌بندد (نه قطع خام TCP)؛ `EventSource` مرورگر طبق رفتار پیش‌فرضش سعی به reconnect می‌کند و چون کوکی همان توکن منقضی را دوباره می‌فرستد، `get_token_payload` دوباره `401` برمی‌گرداند — یعنی از این به بعد چرخه‌ی «توکن منقضی = اتصال واقعاً قطع» کامل شد (نه فقط برای اتصال‌های جدید، همان‌طور که در `SSE_REVIEW.md` به‌عنوان مشکل فهرست شده بود).
- اگر یک مصرف‌کننده عقب بیفتد و صف‌اش پر شود، دیگر پیام بی‌صدا دور ریخته نمی‌شود؛ اتصال با یک پایان تمیز بسته می‌شود تا کلاینت (یا یک بار بعدی که وصل می‌شود) بداند عقب افتاده، به‌جای این‌که سایلنت events را از دست بدهد.
