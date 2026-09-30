-- BHASHASETU visit log. Run once in the D1 console (Storage & Databases > D1 > bhashasetu_analytics > Console).
-- One row per page or worksheet request. City, region, country and ISP are resolved by
-- Cloudflare from the visitor's IP; times are stored in UTC.

CREATE TABLE IF NOT EXISTS hits (
  id       INTEGER PRIMARY KEY AUTOINCREMENT,
  ts       TEXT    NOT NULL,   -- UTC, 'YYYY-MM-DD HH:MM:SS'
  status   INTEGER NOT NULL,   -- 200 served, 404 missing page
  path     TEXT    NOT NULL,   -- e.g. /courses/bengali_to_hindi
  ip       TEXT,
  city     TEXT,
  region   TEXT,               -- state, e.g. West Bengal
  country  TEXT,               -- two-letter code, e.g. IN
  isp      TEXT,               -- network, e.g. Reliance Jio
  device   TEXT,               -- mobile / tablet / desktop / bot
  browser  TEXT,
  os       TEXT,
  referer  TEXT,               -- where the visitor came from
  ua       TEXT                -- raw user agent, kept for checking bots
);

-- One index only: every index adds a written row per visit, and D1's free plan
-- allows 100,000 written rows a day.
CREATE INDEX IF NOT EXISTS idx_hits_ts ON hits (ts);
