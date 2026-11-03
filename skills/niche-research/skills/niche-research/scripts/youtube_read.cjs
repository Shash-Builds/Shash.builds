#!/usr/bin/env node
// Reads public YouTube pages in a real browser, at human pace, and prints JSON.
//
//   node youtube_read.cjs "https://www.youtube.com/results?search_query=..."   videos on a search page
//   node youtube_read.cjs "https://www.youtube.com/@channel/videos"            videos on a channel page
//   node youtube_read.cjs "https://www.youtube.com/watch?v=ID"                 one video: exact date, views, length
//   node youtube_read.cjs "https://www.youtube.com/@channel/about"             channel: subscribers as shown
//
// Needs Node.js and Playwright with Chromium. It never logs in, and reports
// {"blocked": true} instead of getting around a consent or bot page.
let chromium;
try { ({ chromium } = require("playwright")); } catch (e) {
  console.log(JSON.stringify({ error: "Playwright is not installed: npm i playwright, then npx playwright install chromium" }));
  process.exit(1);
}
const url = process.argv[2];
if (!url || !/^https:\/\/(www\.|m\.)?youtube\.com\//.test(url)) {
  console.log(JSON.stringify({ error: "give one https://www.youtube.com/ URL" }));
  process.exit(2);
}

(async () => {
  let browser;
  const out = { url, fetched_at: new Date().toISOString(), blocked: false };
  try {
    browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
    const page = await browser.newPage({ locale: "en-US", extraHTTPHeaders: { "Accept-Language": "en-US,en;q=0.9" } });
    const res = await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
    out.status = res ? res.status() : null;
    await page.waitForTimeout(2500);
    if (/consent\.youtube|google\.com\/sorry/.test(page.url()) || (out.status && out.status >= 400)) {
      out.blocked = true;
    } else if (/\/watch\?/.test(url)) {
      Object.assign(out, await page.evaluate(() => {
        const p = window.ytInitialPlayerResponse || {};
        const v = p.videoDetails || {}, m = (p.microformat || {}).playerMicroformatRenderer || {};
        return { title: v.title || null, channel: v.author || null, channel_url: m.ownerProfileUrl || null,
                 views: v.viewCount ? Number(v.viewCount) : null, length_s: v.lengthSeconds ? Number(v.lengthSeconds) : null,
                 published: (m.publishDate || m.uploadDate || "").slice(0, 10) || null,
                 description: (v.shortDescription || "").slice(0, 400) };
      }));
      if (!out.published) {  // the player is often held behind a bot check; the page source still has the facts
        const html = await page.content();
        const pick = (re) => { const m = html.match(re); return m ? m[1] : null; };
        out.title = out.title || pick(/"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"/);
        out.channel = out.channel || pick(/"ownerChannelName":"((?:[^"\\]|\\.)*)"/) ||
          pick(/"videoOwnerRenderer":\{.*?"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"/);
        const views = pick(/"originalViewCount":"(\d+)"/) || (pick(/"viewCount":\{"simpleText":"([\d,]+) views"/) || "").replace(/,/g, "");
        out.views = out.views || (views ? Number(views) : null);
        const shown = pick(/"publishDate":\{"simpleText":"([^"]+)"/) || pick(/"dateText":\{"simpleText":"([^"]+)"/);
        const d = shown && /\d{4}/.test(shown) ? new Date(shown + " UTC") : null;
        out.published = d && !isNaN(d) ? d.toISOString().slice(0, 10) : null;
        out.published_shown = shown;
        const ms = pick(/"approxDurationMs":"(\d+)"/);
        out.length_s = out.length_s || (ms ? Math.round(Number(ms) / 1000) : null);
      }
    } else if (/\/about\b/.test(url) || /\/@[^/]+\/?$/.test(url)) {
      const text = await page.evaluate(() => document.body.innerText);
      const subs = text.match(/([\d.,]+\s*[KMB]?)\s+subscribers/i);
      const vids = text.match(/([\d.,]+\s*[KMB]?)\s+videos/i);
      Object.assign(out, { title: await page.title(), subscribers_shown: subs ? subs[1] : null, videos_shown: vids ? vids[1] : null });
    } else {
      for (let i = 0; i < 2; i++) { await page.mouse.wheel(0, 4000); await page.waitForTimeout(1200); }
      out.videos = await page.evaluate(() => {
        const seen = new Set(), rows = [];
        for (const a of document.querySelectorAll('a#video-title, a#video-title-link, a[href*="/shorts/"]')) {
          const href = a.href.split("&")[0];
          if (!/\/(watch\?v=|shorts\/)[\w-]{6,}/.test(href) || seen.has(href)) continue;
          seen.add(href);
          const box = a.closest("ytd-video-renderer, ytd-rich-item-renderer, ytd-grid-video-renderer, ytd-reel-item-renderer") || a.parentElement;
          const meta = box ? [...box.querySelectorAll("#metadata-line span, .inline-metadata-item")].map((s) => s.textContent.trim()) : [];
          const ch = box && box.querySelector("ytd-channel-name a, #channel-name a");
          rows.push({ title: (a.getAttribute("title") || a.textContent || "").trim(), url: href,
                      channel: ch ? ch.textContent.trim() : null, shown: meta.filter(Boolean) });
          if (rows.length >= 40) break;
        }
        return rows;
      });
    }
  } catch (e) {
    out.error = String(e.message || e).split("\n")[0];
  } finally {
    if (browser) await browser.close();
  }
  console.log(JSON.stringify(out, null, 1));
})();
