# Build log

Last update: 2026-11-03

## Done

- **2026-11-03. Offer terms confirmed** and applied to [offer-page.md](research/offer-page.md) and [marketplace-kit.md](research/marketplace-kit.md): 50% deposit, 2 revisions, hosting free for a month then $10/month, refunds only for a missed 7-day deadline or undelivered work. Level-Up Dashboard now has its Make-a-copy link.
- **2026-11-03. Sales kit + research (brief from Mother chat, all 9 items).**
  - Skills: [Lead Finder](skills/lead-finder), [Site Audit](skills/site-audit), [Mock Builder](skills/mock-builder), [Cold Email Drafter](skills/cold-email-drafter), run in order by a new Master **Sales head**. Offline tests added; tested on real public sites (results not committed).
  - [Level-Up Dashboard Sheet template](tools/level-up-dashboard): 6 tabs (days, sales, content, followers, reviews, config).
  - Research: [cold email US](research/cold-email-us.md), [marketplace kit](research/marketplace-kit.md), [course platforms](research/course-platforms.md), [offer page copy](research/offer-page.md).
  - Community post copy: [content/drops/2026-11-03-sales-kit.md](content/drops/2026-11-03-sales-kit.md).
- **2026-11-03. Two web tools open-sourced:** [One-Page Starter](tools/one-page-starter) (one-page site per business from a CSV, optional preview ribbon, `--sheet-url` live form) and [Lead Tracker](tools/lead-tracker) (form leads into a Google Sheet with source and a Dashboard). Both with demos. The starter's demo is now in the README's first screen.
- **2026-11-03. 14 Claude skills open-sourced** in [`skills/`](skills/): Master, Humanizer, Social Media, LinkedIn, Motion Design Taste, Audio Review, Transcriber, Clipper, AI Visuals, Harsh Buyer Review, Competitor Research, Ecom, Careful Mode, Economy Mode. Installable as a Claude Code plugin catalog (`shashbuilds`), each with its own README and header, relicensed to Shashwat Jain, full test suite in CI. Release notes ready for tag `skills-v1.0.0`.
- **2026-11-03. Front door.** README, media kit (banner, animated Tab, icons, social preview, per-item headers, all built by `media/build.py`), LICENSE (MIT) plus LICENSE-CONTENT (CC BY 4.0), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue forms (bug, idea, hire), PR template, `llms.txt`, `AGENTS.md`, `catalog.json`, a repo check (`scripts/check.py`, runs in CI) and a release workflow (push a tag, get a Release with notes and a zip).
- **2026-11-03. Communities map.** [`research/communities.md`](research/communities.md): 59 places, ranked, with rules, sources and a launch-day playbook.
- **2026-11-03. Profile README** drafted in [`profile/README.md`](profile/README.md).

## In progress

- Nothing open. Next session starts on the video template.

## Next

Open-sourcing everything, in waves:

- Wave 3 (needs Shashwat to create empty repos): the reel engine, the OSE web platform, the Instagram client.
- A new shash.builds demo video for the README, made with the Master Skill's video workflow.

Standing jobs:

1. Video template (`templates/video/`), standing job 4.
2. Seed the repo from `briefs/seed/` (waiting for the export).
3. 30-day content calendar from 2026-11-04 (waiting for the topic list).
4. First autopilot drop from the backlog below.

## Backlog: free drops (one every 1 to 2 days)

| # | Drop | Kind | Who it helps |
| --- | --- | --- | --- |
| 2 | Homepage teardown skill: scores a homepage and drafts a before/after redesign brief | skill | Web designers |
| 3 | Local business schema generator: JSON-LD for LocalBusiness, services and FAQ | tool | Anyone with a local site |
| 4 | Review link and QR maker for a Google Business Profile | tool | Service businesses |
| 5 | Service-area page writer skill that avoids thin, duplicate city pages | skill | Service businesses, SEO folks |
| 6 | Quote calculator widget (drop-in, no backend) | tool | Cleaners, painters, detailers |
| 7 | Speed and SEO pre-launch checklist skill | skill | Web designers |
| 8 | Client onboarding questionnaire for one-page sites | template | Web designers |

Before building any of these, check the seed export so nothing gets built twice.

## Blocked

- Seed export not in `briefs/seed/` yet.
- 30-day calendar needs the topic list.

## Budget

Rough estimate: about 22% of the weekly limit used this week (front door, media kit, skills port; research and READMEs done by Haiku and Sonnet helpers). Stop and report at 45%.

## Questions for Mother chat

- **Dashboard columns.** The Sheet template uses default headers (listed in its README). Send the dashboard's real column list if it differs.
- **Offer page leftovers** in `research/offer-page.md`: payment method, call length, intake list, post-launch changes, and whether site files are handed over at launch or on cancelling hosting. Still marked `[[REAL: ...]]`.
- **Contra fees** conflict between Contra's own help pages (0% vs $15 per payment under $500). Check with Contra support before listing.

1. **Rename OK?** Can the GitHub account become `ShashwatBuilds` and this repo `shash.builds`? All badges and links already point there and go live after the rename.
2. **Website URL.** What's the shash.builds site address? The README's hire section uses LinkedIn and an issue form until then.
3. **Public business email.** Is there one to list? Until then, contact is LinkedIn only.
4. **Needs Shashwat's clicks** (no API access from here): in repo Settings, set the description, topics, social preview (`media/social-preview.png`), turn on Actions and private vulnerability reporting. Text is below.
5. **Publish the skills release:** after the rename, push the tags: `skills-v1.0.0`, `one-page-starter-v1.0.0`, `lead-tracker-v1.0.0`. The workflow builds and attaches every zip. (I can push them once Actions is on.)
6. **Profile README:** the profile repo must be named exactly like the account (`ShashwatBuilds/ShashwatBuilds`). OK to rename the existing profile repo to that after the account rename? The README is ready in `profile/README.md`.

### Paste-ready repo settings

- **Description:** Free Claude skills and open-source web tools for US service businesses and web designers. Built in public by Shashwat Jain.
- **Topics:** `claude` `claude-code` `claude-skills` `anthropic` `ai-agents` `web-design` `one-page-website` `website-templates` `small-business` `local-seo` `build-in-public` `open-source` `freelance` `html-css`
- **Social preview:** upload `media/social-preview.png`.
