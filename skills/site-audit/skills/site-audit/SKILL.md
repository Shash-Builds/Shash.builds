---
name: site-audit
description: Audit a small business website for a sales pitch: weak-site score 0-100 and the 3 most specific provable problems (phone layout, speed, call button, reviews, service area, https, broken links, Google profile) in plain words. Use for "audit this site", "is this website weak", or before cold outreach.
---

# Site Audit

Score how weak a small business website is and name the 3 problems an owner would care
about, with proof. Facts only: never guess, never judge taste without evidence.

## 1. Run the audit

```
python3 ${CLAUDE_SKILL_DIR}/scripts/audit.py <url or "none"> --name "<business>" --md audit.md > audit.json
```

(`scripts/audit.py` is next to this SKILL.md.) It reads robots.txt and stops if the page is
disallowed, fetches the one page, and sends HEAD requests to at most 15 of its links (skip
with `--no-links`). Python 3 standard library only.

## 2. Read the result

- `score`: 0 to 100, higher means a weaker site (a better prospect for a rebuild).
- `problems`: each has a plain sentence and its `evidence`. `top_3` are the heaviest.
- `facts`: what was measured (https, download time from the audit server, viewport, tel links,
  action buttons, links checked).
- `skipped`: robots.txt asked tools not to fetch the page. Respect it; do not work around it.

## 3. Report

Give the score and the top 3 problems, each in one sentence a business owner understands,
with its evidence. Download time is from the audit server, not a phone: say so if you quote
it. If the user wants a design opinion ("outdated"), only add it with something visible as
proof (a screenshot, a copyright year, old tags). Never invent a problem to fill 3 slots.

## 4. Hand-offs

The audit JSON feeds `mock-builder` (what to fix in the mock) and `cold-email-drafter`
(the one personal line). `lead-finder` runs this audit on every business it finds.
