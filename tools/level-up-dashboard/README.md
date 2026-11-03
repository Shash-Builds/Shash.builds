<p align="center"><img src="header.svg" width="100%" alt="Level-Up Dashboard header: a shash.builds web tool. Track a build-in-public run: days, sales, content, followers."></p>

# Level-Up Dashboard

**One Google Sheet that tracks a build-in-public run day by day: hours, what shipped, outreach, sales, posts, followers and real reviews.**

This folder holds the Sheet template. A live dashboard page that reads it is in the [backlog](../../STATUS.md).

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

## Rules that keep it honest

- Numbers come from each platform's own analytics or your bank, never from memory.
- A review goes public only when `permission_to_share` is `yes`.
- Client names stay in your copy. Don't publish the `sales` tab.

## FAQ

**Why a Sheet?** It's free, it works on a phone, and you can share it read-only with anyone, or with an assistant.

**Can I add columns?** Yes. Add them at the end of a tab so anything that reads the headers keeps working.

## Changelog

- **0.1.0** (2026-11-03): the Sheet template.

---

Made by [shash.builds](../../README.md). Need a one-page website for your service business? [$400 flat, live in 7 days](../../README.md#hire-me).

MIT licensed, copyright Shashwat Jain.
