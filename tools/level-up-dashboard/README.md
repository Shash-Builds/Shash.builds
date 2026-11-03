<p align="center"><img src="header.svg" width="100%" alt="Level-Up Dashboard header: a shash.builds web tool. Track a build-in-public run: days, sales, content, followers."></p>

# Level-Up Dashboard

**One Google Sheet that tracks a build-in-public run day by day: hours, what shipped, outreach, sales, posts, followers and real reviews.**

It has two parts:

- **The Sheet template** (below): where your numbers live.
- **The app** ([`docs/level-up/`](../../docs/level-up/index.html)): a phone-first page to log your day and see your level, XP, streak, and money against your pace. It talks to your Sheet through a small script you paste into it ([`apps-script/Code.gs`](apps-script/Code.gs)), protected by a passphrase you choose.

Your goals, pace and XP weights live in the Sheet's `config` tab, not in code, so anyone can set their own target and chase it.

## The Sheet template

Six tabs, one header row each, frozen and styled. Nothing else to set up.

| Tab | One row per | Columns |
| --- | --- | --- |
| `days` | day | date, day, hours_worked, shipped, outreach_sent, replies, calls_booked, posts_published, notes |
| `sales` | payment | date, client, offer, amount_usd, status (deposit, paid, refunded), source, notes |
| `content` | post | date, platform, format, title, url, views, likes, comments, shares, saves |
| `followers` | check-in | date, instagram, youtube, linkedin, x, github_stars |
| `reviews` | real review | date, client, platform, rating, quote, permission_to_share (yes, no), url |
| `config` | setting | key, value, notes: start_date, goal_usd, offer_price_usd, timezone, currency |

## Install in 3 steps

1. **[Make a copy of the Google Sheet](https://docs.google.com/spreadsheets/d/14H1zb1JAfK5d10UuI4kJBvFVKrOCVYIU_aScMdlTp5A/copy)** (you need a Google account).
2. Set your `start_date` and `goal_usd` in the `config` tab.
3. Add a row to `days` every evening.

No Google account? Download [`sheet-template/level-up-dashboard.xlsx`](sheet-template/level-up-dashboard.xlsx) and open it in Excel or any spreadsheet app.

Prefer plain files? Each tab is also a CSV in [`sheet-template/`](sheet-template).

## The app in 4 steps

1. In your copy of the Sheet: Extensions, then Apps Script. Paste [`apps-script/Code.gs`](apps-script/Code.gs) and save.
2. Project Settings, then Script Properties: add `PASSPHRASE` with a long phrase only you know.
3. Deploy, then New deployment, then Web app (Execute as: Me, Who has access: Anyone). Copy the `/exec` URL.
4. Open the app ([shash-builds.github.io/Shash.builds/level-up/](https://shash-builds.github.io/Shash.builds/level-up/), or host `docs/level-up/index.html` yourself), paste the URL and passphrase, and tap Unlock.

Every read and every write needs the passphrase, so the URL alone shows nothing. The URL and passphrase are saved only on your device.

**How the game works.** XP per day = hours x `xp_hour` (10) + outreach x `xp_outreach` (2) + replies x `xp_reply` (5) + calls x `xp_call` (20) + posts x `xp_post` (10) + `xp_ship` (25) if you shipped something, plus `xp_per_usd` (0.5) per dollar earned. Level 1 needs `level_base` (100) XP, and each level after needs `level_step` (50) more. A streak counts consecutive logged days. Pace is `goal_usd` spread evenly over `goal_days` (30) from `start_date`. Change any number in the `config` tab.

## Rules that keep it honest

- Numbers come from each platform's own analytics or your bank, never from memory.
- A review goes public only when `permission_to_share` is `yes`.
- Client names stay in your copy. Don't publish the `sales` tab.

## FAQ

**Why a Sheet?** It's free, it works on a phone, and you can share it read-only with anyone, or with an assistant.

**Can I add columns?** Yes. Add them at the end of a tab so anything that reads the headers keeps working.

## Changelog

- **0.2.0** (2026-11-03): the app (daily log, level, XP, streak, money vs pace) and the Apps Script API.
- **0.1.0** (2026-11-03): the Sheet template.

---

Made by [shash.builds](../../README.md). Need a one-page website for your service business? [$400 flat, live in 7 days](../../README.md#hire-me).

MIT licensed, copyright Shashwat Jain.
