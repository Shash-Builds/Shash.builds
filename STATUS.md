# Build log

Last update: 2026-11-03

## Done

- **2026-11-03. 14 Claude skills open-sourced** in [`skills/`](skills/): Master, Humanizer, Social Media, LinkedIn, Motion Design Taste, Audio Review, Transcriber, Clipper, AI Visuals, Harsh Buyer Review, Competitor Research, Ecom, Careful Mode, Economy Mode. Installable as a Claude Code plugin catalog (`shashbuilds`), each with its own README and header, relicensed to Shashwat Jain, full test suite in CI. Release notes ready for tag `skills-v1.0.0`.
- **2026-11-03. Front door.** README, media kit (banner, animated Tab, icons, social preview, per-item headers, all built by `media/build.py`), LICENSE (MIT) plus LICENSE-CONTENT (CC BY 4.0), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue forms (bug, idea, hire), PR template, `llms.txt`, `AGENTS.md`, `catalog.json`, a repo check (`scripts/check.py`, runs in CI) and a release workflow (push a tag, get a Release with notes and a zip).
- **2026-11-03. Communities map.** [`research/communities.md`](research/communities.md): 59 places, ranked, with rules, sources and a launch-day playbook.
- **2026-11-03. Profile README** drafted in [`profile/README.md`](profile/README.md).

## In progress

- Nothing open. Next session starts on the video template.

## Next

Open-sourcing everything, in waves:

- Wave 2: tools in this hub: the one-page preview template and the lead tracker Sheets kit.
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
| 1 | One-page starter: a single-file site for a local service business (hero, services, reviews, service area, call button, form) | tool | Service businesses, web designers |
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

Rough estimate: about 12% of the weekly limit used this week (front door, media kit, skills port; research and READMEs done by Haiku and Sonnet helpers). Stop and report at 45%.

## Questions for Mother chat

1. **Rename OK?** Can the GitHub account become `ShashwatBuilds` and this repo `shash.builds`? All badges and links already point there and go live after the rename.
2. **Website URL.** What's the shash.builds site address? The README's hire section uses LinkedIn and an issue form until then.
3. **Public business email.** Is there one to list? Until then, contact is LinkedIn only.
4. **Needs Shashwat's clicks** (no API access from here): in repo Settings, set the description, topics, social preview (`media/social-preview.png`), turn on Actions and private vulnerability reporting. Text is below.
5. **Publish the skills release:** after the rename, push the tag: `git tag skills-v1.0.0 && git push origin skills-v1.0.0`. The workflow builds and attaches every zip.
6. **Profile README:** the profile repo must be named exactly like the account (`ShashwatBuilds/ShashwatBuilds`). OK to rename the existing profile repo to that after the account rename? The README is ready in `profile/README.md`.

### Paste-ready repo settings

- **Description:** Free Claude skills and open-source web tools for US service businesses and web designers. Built in public by Shashwat Jain.
- **Topics:** `claude` `claude-code` `claude-skills` `anthropic` `ai-agents` `web-design` `one-page-website` `website-templates` `small-business` `local-seo` `build-in-public` `open-source` `freelance` `html-css`
- **Social preview:** upload `media/social-preview.png`.
