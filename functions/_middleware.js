// Visit logger for BHASHASETU on Cloudflare Pages.
//
// Runs in front of every request, serves the page exactly as before, and afterwards writes one
// row to the D1 database bound as DB: time, page, IP address, city, region, country, network
// (ISP), device, browser and operating system.
//
// City, region, country and ISP are resolved by Cloudflare itself from the visitor's IP and
// handed to us on request.cf, so no outside geolocation service is called.
//
// Logging can never break the site: it runs after the response is sent (waitUntil), every
// database error is swallowed, and if no DB is bound (for example on preview deployments)
// nothing is logged at all.

const SKIP = /\.(ico|png|jpe?g|gif|svg|webp|css|js|map|woff2?|ttf|txt|xml|json)$/i;

function device(ua) {
  if (!ua || /bot|crawl|spider|slurp|facebookexternalhit|preview|headless|python|curl|wget/i.test(ua)) return "bot";
  if (/iPad|Tablet/i.test(ua) || (/Android/i.test(ua) && !/Mobile/i.test(ua))) return "tablet";
  if (/Mobi|iPhone|iPod/i.test(ua)) return "mobile";
  return "desktop";
}

function browser(ua) {
  if (/Edg\//.test(ua)) return "Edge";
  if (/OPR\/|Opera/.test(ua)) return "Opera";
  if (/SamsungBrowser/.test(ua)) return "Samsung Internet";
  if (/Firefox\/|FxiOS/.test(ua)) return "Firefox";
  if (/Chrome\/|CriOS/.test(ua)) return "Chrome";
  if (/Safari\//.test(ua)) return "Safari";
  return "other";
}

function os(ua) {
  // Order matters: Android user agents also say Linux, and iOS ones say "like Mac OS X".
  if (/Android/.test(ua)) return "Android";
  if (/iPhone|iPad|iPod/.test(ua)) return "iOS";
  if (/Windows/.test(ua)) return "Windows";
  if (/Mac OS X|Macintosh/.test(ua)) return "macOS";
  if (/CrOS/.test(ua)) return "ChromeOS";
  if (/Linux/.test(ua)) return "Linux";
  return "other";
}

function readablePath(pathname) {
  try { return decodeURIComponent(pathname); } catch { return pathname; }
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const response = await next();

  const url = new URL(request.url);
  const status = response.status;
  const loggable =
    env.DB &&
    request.method === "GET" &&
    !SKIP.test(url.pathname) &&
    // Pages redirects /page.html to /page; logging both would count every visit twice.
    !(status >= 300 && status < 400);

  if (loggable) {
    const ua = request.headers.get("user-agent") || "";
    const cf = request.cf || {};
    const ts = new Date().toISOString().replace("T", " ").slice(0, 19); // UTC, SQLite format

    context.waitUntil(
      env.DB.prepare(
        `INSERT INTO hits (ts, status, path, ip, city, region, country, isp, device, browser, os, referer, ua)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
      )
        .bind(
          ts,
          status,
          readablePath(url.pathname),
          request.headers.get("CF-Connecting-IP"),
          cf.city || null,
          cf.region || null,
          cf.country || null,
          cf.asOrganization || null,
          device(ua),
          browser(ua),
          os(ua),
          request.headers.get("referer"),
          ua.slice(0, 400)
        )
        .run()
        .catch(() => {})
    );
  }

  return response;
}
