# Build log

Last update: 2026-11-06

## Done

- **2026-11-06. Agent Team skill** ([`skills/agent-team`](skills/agent-team)): one head chat runs a team of specialist Claude agents, each with its own folder, git branch, best-of skill playbook and inbox in one private repo; a training block for every agent; daily briefing and hard review by the head. Templates in `templates.md`. Routed from the Marketing head. 23 skills now.
- **2026-11-05. Front door reframed as "stuff I built".** README tagline, "What this is", profile README, `llms.txt` and the banner, social preview and profile header no longer say web design is the paid work. The portfolio, templates and the "Hire me" section stay, so a site can still be bought.
- **2026-11-04. Portfolio:** 8 concept sites, one per trade and style, with case cards, screenshots, scroll videos and a marketplace pack. Gallery: https://shash-builds.github.io/Shash.builds/portfolio/ (source in `portfolio/`, Pages copy in `docs/portfolio/`).
- **2026-11-04. Comment Drafter skill** ([`skills/comment-drafter`](skills/comment-drafter)): two comment drafts per post for LinkedIn, X or Instagram, in the user's voice; drafts only, never posts or logs in. Routed from the Marketing head. 22 skills now.
- **2026-11-04. Brutal Review skill** ([`skills/brutal-review`](skills/brutal-review)): a blunt second opinion from a different model, original code and prompts, privacy redaction, tests and chaos inputs. 21 skills now.
- **2026-11-04. AI Resume skill** ([`skills/ai-resume`](skills/ai-resume)): true, one-page, ATS-safe resumes with Hallmark and humanizer checks; sample resume with made-up data; routed by the Master Design head. 20 skills now.
- **2026-11-04. Level-Up Game 15-day plan panel** and **email instead of LinkedIn** across the site and docs.
- **2026-11-04. Level-Up Game Dashboard open-sourced** in [`tools/level-up-dashboard/`](tools/level-up-dashboard): one HTML file with a `CONFIG` block (levels, quests, XP, money pace, mini-boss, products, channels, role model label), storage in the user's private Claude artifact or the browser (Export/Import), and a sample mode. Personal parts left out (job-hunt tab, personal targets, names). Skill: [`SKILL.md`](tools/level-up-dashboard/SKILL.md). Example config: [`one-page-studio.config.js`](tools/level-up-dashboard/game/examples/one-page-studio.config.js). Live sample: `docs/level-up-game/` (needs Pages on). Agensi listing and cover in `agensi/`, **not published** until Shashwat approves. LinkedIn draft: [`content/drops/2026-11-05-level-up-game.md`](content/drops/2026-11-05-level-up-game.md).
- **2026-11-03. Level-Up Dashboard app v1:** phone-first page in [`docs/level-up/`](docs/level-up/index.html) (daily log, level, XP, streak, money vs pace) on top of Shashwat's Sheet through [`apps-script/Code.gs`](tools/level-up-dashboard/apps-script/Code.gs). Passphrase on every read and write; nothing personal in the repo. Goals, pace and XP weights come from the Sheet's `config` tab, ready for the generic "Role Model" version. Served by GitHub Pages from `/docs` on this branch.
- **2026-11-03. Seed export + Niche Research** (from branch chat 2), merged after a privacy, brand and size review (30 binaries, 2.7 MB total, none over 500 KB).
  - [`briefs/seed/`](briefs/seed): the site (index, lookbook, skills page), the booked-one-pager skill draft, Tab mascot stills and loops, trailer scenes, Built in Bed graphics. See its `MANIFEST.md` for sources and the 5 open items.
  - [Niche Research](skills/niche-research) skill (19 skills now), with the shash.builds niche run in [`research/niche/shash-builds/report.md`](research/niche/shash-builds/report.md). Drop copy: [content/drops/niche-research.md](content/drops/niche-research.md).
  - Release plan: one first release, `skills-v1.0.0`, covers all 19 skills (the separate v1.1.0 notes were folded in).
- **2026-11-03. Toolbox batch 1** in [`tools/toolbox/`](tools/toolbox): local CLI tools that are also Claude skills, with installers for macOS/Linux and Windows. Tested on Linux; Windows untested until Shashwat runs the checklist.
  - [transcribe](tools/toolbox/transcribe), [cut-silence](tools/toolbox/cut-silence), [video-build](tools/toolbox/video-build), [repurpose](tools/toolbox/repurpose), [photo-kit](tools/toolbox/photo-kit). Release notes ready for tags `<tool>-v0.1.0`.
  - Agensi packages are in each tool's `agensi/` folder, prepared only; each waits for Shashwat's approval.
  - Transcriber engine: medium and large-v3 sizes, `--max-chars`, joined word pieces. Fixed its environment variable names (`SHASHBUILDS_WHISPER_CACHE`, `SHASHBUILDS_WHISPER_REGISTRY`).
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

- Toolbox batch 2 (thumb-maker, carousel-maker, site-snap, og-favicon, invoice, utm-link) on `claude/toolbox`.
- Video template (`templates/video/`) will call `tools/toolbox/video-build` and add the brand layer.

## Next

- **Role Model avatar**: a stylized 3D figure on the desktop game that evolves with level (queued, waits for HEAD's go).
Open-sourcing everything, in waves:

- Wave 3 (needs Shashwat to create empty repos): the reel engine, the OSE web platform, the Instagram client.
- A new shash.builds demo video for the README, made with the Master Skill's video workflow.

Standing jobs:

0. Sort `briefs/seed/` into the layout (site to its own home, Tab assets to `media/`, booked-one-pager to `skills/`), standing job 2.
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

- **Binary exception (approved by Shashwat, 2026-11-03):** `scroll.mp4` files under `portfolio/*/shots/` stay in git (8 files, about 11 MB). Everything else keeps the rule: no video or audio in git, and flag any batch over about 15 MB.
- **Windows test of the toolbox** (checklist in the toolbox branch chat).
- **Releases to cut after the rename:** `skills-v1.0.0`, `one-page-starter-v1.0.0`, `lead-tracker-v1.0.0`, and `transcribe`, `cut-silence`, `video-build`, `repurpose`, `photo-kit` at `-v0.1.0`.
- **Dashboard columns.** The Sheet template uses default headers (listed in its README). Send the dashboard's real column list if it differs.
- **Offer page leftovers** in `research/offer-page.md`: call length, intake list, post-launch changes, and whether site files are handed over at launch or on cancelling hosting. Still marked `[[REAL: ...]]`.
- **Contra fees** conflict between Contra's own help pages (0% vs $15 per payment under $500). Check with Contra support before listing.

1. **Rename:** done. The account is `Shash-Builds`; every link points to github.com/Shash-Builds/shash.builds.
2. **Website URL:** https://shashwat-websites.netlify.app, now in the README, profile README and llms.txt.
3. **Public business email:** shash.builds@gmail.com, now in the README, the profile README and the offer page.
4. **Needs Shashwat's clicks** (no API access from here): in repo Settings, set the description, topics, social preview (`media/social-preview.png`), turn on Actions and private vulnerability reporting. Text is below.
5. **Publish the skills release:** after the rename, push the tags: `skills-v1.0.0`, `one-page-starter-v1.0.0`, `lead-tracker-v1.0.0`. The workflow builds and attaches every zip. (I can push them once Actions is on. Waiting for the go.)
6. **Profile README:** the profile repo must be named exactly like the account (`Shash-Builds/Shash-Builds`). The README is ready in `profile/README.md`.

### Paste-ready repo settings

- **Description:** Free Claude skills and open-source web tools for US service businesses and web designers. Built in public by Shashwat Jain.
- **Topics:** `claude` `claude-code` `claude-skills` `anthropic` `ai-agents` `web-design` `one-page-website` `website-templates` `small-business` `local-seo` `build-in-public` `open-source` `freelance` `html-css`
- **Social preview:** upload `media/social-preview.png`.
