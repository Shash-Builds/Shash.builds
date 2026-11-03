// Screenshots and a scroll video for each concept site, for the gallery and the marketplaces.
//   node portfolio/shots.cjs roofer-tx [cleaner-fl ...]
// Writes portfolio/<slug>/shots/:
//   desktop-1600x1200.jpg  Dribbble, Upwork, Contra cover
//   mobile-1080x1350.jpg   Instagram portrait: the phone screen on the brand color (ig_bg in site.json)
//   mobile-390x844.png     the raw phone screen at 2x
//   desktop-1280x720.jpg   Fiverr cover, link previews
//   scroll.mp4             1280x720 scroll through the whole page
// Needs Playwright with Chromium and ffmpeg.
const { chromium } = require('playwright');
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const SHOTS = [
  ['desktop-1600x1200.jpg', 1280, 960, 1.25],
  ['desktop-1280x720.jpg', 1280, 720, 1],
];

async function ready(page) {
  await page.evaluate(() => document.querySelectorAll('img[loading]').forEach((i) => i.removeAttribute('loading')));
  await page.evaluate(() => document.fonts.ready);
  await page.waitForLoadState('networkidle');
  await page.waitForTimeout(900); // let the hero entrance finish
}

async function shoot(browser, slug) {
  const url = 'file://' + path.join(ROOT, slug, 'index.html');
  const out = path.join(ROOT, slug, 'shots');
  fs.mkdirSync(out, { recursive: true });
  for (const [name, w, h, scale] of SHOTS) {
    const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
    await page.goto(url);
    await ready(page);
    await page.screenshot({ path: path.join(out, name), type: 'jpeg', quality: 88 });
    await page.close();
  }
  // phone screen, then centred on the brand color at 1080x1350 (ImageMagick)
  const phone = path.join(out, 'mobile-390x844.png');
  const pg = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await pg.goto(url);
  await ready(pg);
  await pg.screenshot({ path: phone });
  await pg.close();
  const bg = JSON.parse(fs.readFileSync(path.join(ROOT, slug, 'site.json'), 'utf8')).ig_bg || '#111111';
  const ph = path.join(out, '.phone.png'), mask = path.join(out, '.mask.png');
  execFileSync('convert', ['-size', '540x1170', 'xc:none', '-fill', 'white', '-draw', 'roundrectangle 0,0 539,1169 44,44', mask]);
  execFileSync('convert', [phone, '-resize', '540x1170', '-alpha', 'set', mask, '-compose', 'DstIn', '-composite', '-compose', 'over',
    '(', '+clone', '-background', 'black', '-shadow', '40x22+0+16', ')', '+swap', '-background', 'none', '-layers', 'merge', '+repage', ph]);
  execFileSync('convert', ['-size', '1080x1350', 'xc:' + bg, ph, '-gravity', 'center', '-compose', 'over', '-composite', '-quality', '88', path.join(out, 'mobile-1080x1350.jpg')]);
  fs.rmSync(mask);
  fs.rmSync(ph);
  // scroll video: record, then convert to H.264 MP4
  const tmp = fs.mkdtempSync(path.join(require('os').tmpdir(), 'scroll-'));
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, recordVideo: { dir: tmp, size: { width: 1280, height: 720 } } });
  const page = await ctx.newPage();
  await page.goto(url);
  await ready(page);
  await page.waitForTimeout(600);
  await page.evaluate(async () => {
    document.documentElement.style.scrollBehavior = 'auto';
    const end = document.documentElement.scrollHeight - innerHeight;
    const dur = Math.min(14000, Math.max(8000, end * 2.2));
    const t0 = performance.now();
    await new Promise((done) => {
      const step = (t) => {
        const k = Math.min(1, (t - t0) / dur);
        const ease = k < 0.5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
        scrollTo(0, end * ease);
        k < 1 ? requestAnimationFrame(step) : done();
      };
      requestAnimationFrame(step);
    });
  });
  await page.waitForTimeout(800);
  const webm = await page.video().path();
  await ctx.close();
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-ss', '1.6', '-i', webm, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'slow', '-r', '30', '-movflags', '+faststart', '-an', path.join(out, 'scroll.mp4')]);
  fs.rmSync(tmp, { recursive: true, force: true });
  console.log('shots', slug);
}

(async () => {
  const slugs = process.argv.slice(2);
  if (!slugs.length) { console.error('usage: node portfolio/shots.cjs <slug> [...]'); process.exit(1); }
  const browser = await chromium.launch();
  for (const s of slugs) await shoot(browser, s);
  await browser.close();
})();
