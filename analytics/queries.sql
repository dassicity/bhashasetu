-- Ready-made queries for the D1 console. Paste one at a time.
-- Times are stored in UTC; these show them in Indian time (UTC + 5:30).
-- Bots are excluded unless the query says otherwise.

-- 1. The last 50 visits: who, where, on what, which page
SELECT datetime(ts, '+5 hours', '+30 minutes') AS time_ist,
       ip, city, region, country, isp, device, browser, os, path
FROM hits
WHERE device != 'bot'
ORDER BY ts DESC
LIMIT 50;

-- 2. Where visitors come from (last 30 days), by city
SELECT city, region, country,
       COUNT(DISTINCT ip) AS visitors,
       COUNT(*)           AS page_views
FROM hits
WHERE device != 'bot' AND status = 200 AND ts >= datetime('now', '-30 days')
GROUP BY city, region, country
ORDER BY visitors DESC
LIMIT 50;

-- 3. By country (last 30 days)
SELECT country,
       COUNT(DISTINCT ip) AS visitors,
       COUNT(*)           AS page_views
FROM hits
WHERE device != 'bot' AND status = 200 AND ts >= datetime('now', '-30 days')
GROUP BY country
ORDER BY visitors DESC;

-- 4. Devices, browsers and operating systems (last 30 days)
SELECT device, os, browser, COUNT(DISTINCT ip) AS visitors
FROM hits
WHERE device != 'bot' AND status = 200 AND ts >= datetime('now', '-30 days')
GROUP BY device, os, browser
ORDER BY visitors DESC;

-- 5. Most visited courses
SELECT path, COUNT(DISTINCT ip) AS visitors, COUNT(*) AS page_views
FROM hits
WHERE path LIKE '/courses/%' AND device != 'bot' AND status = 200
GROUP BY path
ORDER BY visitors DESC;

-- 6. Worksheet PDFs downloaded
SELECT path, COUNT(*) AS downloads, COUNT(DISTINCT ip) AS people
FROM hits
WHERE path LIKE '/worksheets/%.pdf' AND device != 'bot' AND status = 200
GROUP BY path
ORDER BY downloads DESC;

-- 7. Visitors per day (Indian dates)
SELECT date(ts, '+5 hours', '+30 minutes') AS day_ist,
       COUNT(DISTINCT ip) AS visitors,
       COUNT(*)           AS page_views
FROM hits
WHERE device != 'bot' AND status = 200
GROUP BY day_ist
ORDER BY day_ist DESC
LIMIT 60;

-- 8. Everything one IP address did (replace the address)
SELECT datetime(ts, '+5 hours', '+30 minutes') AS time_ist, city, country, device, path, referer
FROM hits
WHERE ip = '203.0.113.7'
ORDER BY ts;

-- 9. Where visitors found the site (external referrers)
--    Replace 'bhashasetu' with a word from YOUR domain, so your own pages are left out.
SELECT referer, COUNT(DISTINCT ip) AS visitors
FROM hits
WHERE referer IS NOT NULL AND referer NOT LIKE '%bhashasetu%' AND device != 'bot'
GROUP BY referer
ORDER BY visitors DESC
LIMIT 30;

-- 10. Broken links people hit
SELECT path, COUNT(*) AS times
FROM hits
WHERE status = 404
GROUP BY path
ORDER BY times DESC;

-- 11. How many rows are stored (the free plan holds 5 GB, roughly millions of visits)
SELECT COUNT(*) AS rows, MIN(ts) AS first_utc, MAX(ts) AS last_utc FROM hits;

-- 12. Housekeeping: delete visits older than 180 days
DELETE FROM hits WHERE ts < datetime('now', '-180 days');
