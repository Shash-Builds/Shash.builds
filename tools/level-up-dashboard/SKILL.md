---
name: level-up-game
description: Turn a 365-day business goal into a game dashboard: levels, boss fights, daily quests, XP, streaks, money against pace, funnel and weekly review. Builds the config from the user's goals and publishes it as their own private Claude artifact with storage, or a file they open in a browser.
---

# Level-Up Game Dashboard

Make the user's year into a game they log every night in under a minute.

## 1. Ask (one message, then build)

- The goal for the year and the money goal with its deadline (for example $10k by day 90).
- What they sell: products with prices.
- Where clients come from: channels, and which are marketplaces or cold outreach.
- Daily habits worth points (outreach, follow-ups, posts, focused work).
- Who they are chasing: a label for the top level ("The Role Model" by default). Use a label only. Never use a real person's photo, likeness or brand.
- Their timezone and currency.

## 2. Build the config

Open `game/level-up-game.html` next to this SKILL.md (Claude Code: `${CLAUDE_SKILL_DIR}/game/level-up-game.html`). Edit only the `CONFIG` block at the top:

- `levels`: 6 to 10 levels, each with a day it is due and `needs` (all must be met). Metrics: `flags`, `sales`, `total`, `bestMonth`, `productSales`, `counter`, `followers`. The last level's name can be `"{roleModel}"`.
- `counters`, `quests` and `xp`: the daily habits, their targets and points.
- `money`: goal, deadline day, unit price and a one-line "math" note with real numbers from the user.
- `miniBoss`: a short first fight (or `null`).
- `plan`: the 15-day plan panel. Keep `enabled: true` and offer to write their first 15 days of tasks; they add them in the panel's editor (one task per line) or you include them in a backup file they import.
- Leave `startDate` empty to start on the day they first open it.

`game/examples/one-page-studio.config.js` is a filled example for a one-page website studio.

Never invent the user's numbers. Ask, or leave the example values and say which ones they should change.

## 3. Deliver

- **Claude artifact (best):** publish the edited file as the user's own private artifact with its database (storage) capability turned on. Saves follow them across devices. The page detects it and says "Saved to your private Claude artifact."
- **Any browser:** give them the file. It saves on that device only and shows Export and Import buttons for backups.
- **Try first:** open it with `#sample` at the end of the address to see made-up sample numbers. Nothing is saved in sample mode.

## 4. Hand-off

Tell them: log every night, Sunday is the weekly review, a 7-day streak doubles XP. Offer to adjust levels after the first two weeks, using their real numbers.
