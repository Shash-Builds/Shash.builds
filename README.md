<p align="center">
  <img src="media/banner.svg" width="100%" alt="shash.builds banner: the wordmark next to Tab, a smiling browser-window mascot with calendar rings and an orange AI spark. One-page websites for US service businesses. Free Claude skills and web tools, built in public.">
</p>

<p align="center">
  <b>I build one-page websites for US service businesses. Everything else I make, I give away here.</b>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT for code, CC BY 4.0 for content" src="https://img.shields.io/badge/license-MIT%20%2B%20CC%20BY%204.0-e8572c?style=flat-square&labelColor=15120f"></a>
  <a href="https://github.com/ShashwatBuilds/shash.builds/commits"><img alt="Last commit" src="https://img.shields.io/github/last-commit/ShashwatBuilds/shash.builds?style=flat-square&color=e8572c&labelColor=15120f"></a>
  <a href="https://github.com/ShashwatBuilds/shash.builds/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/ShashwatBuilds/shash.builds?style=flat-square&color=e8572c&labelColor=15120f"></a>
  <a href="STATUS.md"><img alt="Built in public: read the build log" src="https://img.shields.io/badge/built%20in-public-f6efe3?style=flat-square&labelColor=15120f"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> &nbsp;|&nbsp;
  <a href="#everything-in-here">Skills and tools</a> &nbsp;|&nbsp;
  <a href="#hire-me">Hire me</a> &nbsp;|&nbsp;
  <a href="STATUS.md">Build log</a> &nbsp;|&nbsp;
  <a href="CONTRIBUTING.md">Contribute</a>
</p>

---

## What this is

I'm Shashwat Jain. I'm a web designer in India and I work US hours, 8:30 am to 6:30 pm ET.

My paid work is simple: **a one-page website for a US service business. $400 flat. Live in 7 days.**

This repo is everything around that work, shipped in the open:

- **Claude skills** that do real jobs for small businesses and web designers.
- **Web tools and templates** you can copy, fork and ship today.
- **The build log.** What I built, what broke, what's next. Every day.

All of it is free. Take what helps.

## Quick start

Install any skill in under a minute.

**Claude Code**

```bash
git clone https://github.com/ShashwatBuilds/shash.builds
cp -r shash.builds/skills/<skill-name> ~/.claude/skills/
```

Restart Claude Code. The skill loads on its own when your request matches it.

**Claude.ai (web or desktop)**

1. Download the skill's `.zip` from [Releases](https://github.com/ShashwatBuilds/shash.builds/releases).
2. Open Settings, then Capabilities, then Skills, and upload the zip.
3. Ask Claude for the job the skill does.

**Web tools** are plain HTML, CSS and JavaScript. Open the folder, read its README, deploy it anywhere static (Netlify, Vercel, GitHub Pages).

## Everything in here

<img src="media/icons/skill.svg" width="28" align="left" alt="Claude skill icon: a cream spark on an orange tile.">

### Claude skills

| Skill | What it does | Status |
| --- | --- | --- |
| *The first skills land here this week.* | Each one gets a README, a demo and a release. | Shipping |

<img src="media/icons/tool.svg" width="28" align="left" alt="Web tool icon: a cream wrench on an orange tile.">

### Web tools and templates

| Tool | What it does | Status |
| --- | --- | --- |
| *The first tools land here this week.* | One-page site starters and small tools for service businesses. | Shipping |

What's coming next lives in the backlog in [STATUS.md](STATUS.md). Machines can read the same list in [`catalog.json`](catalog.json) and [`llms.txt`](llms.txt).

## The map

```
skills/      Claude skills: SKILL.md, README, examples, a zip per release
tools/       open-source web tools and one-page site starters
templates/   video, overlay, post and release templates
content/     the daily "Built in Bed" drop: video script, LinkedIn and Instagram posts
media/       banners, icons, Tab, the social preview, and the script that builds them
research/    community maps and platform rules, each with sources and dates
STATUS.md    the public build log
```

## Built in Bed

Every day I post a 2-minute video about what I built that day. The scripts and posts live in [`content/`](content/), one folder per day, so you can see exactly how the sausage gets made.

Meet <img src="media/tab-static.svg" width="22" alt="Tab, the mascot"> **Tab**, the mascot: a browser tab (websites), an AI spark (Claude) and calendar rings (shipped on a schedule).

## Hire me

<img src="media/icons/hire.svg" width="28" align="left" alt="Hire icon: a cream briefcase on an orange tile.">

**One-page website for your service business. $400 flat. Live in 7 days.**

Cleaners, landscapers, painters, contractors, detailers, coaches. If customers find you on Google and call you, you need one clean page that turns that visit into a call.

- Message me on [LinkedIn](https://www.linkedin.com/in/shashbuilds), or
- [Open a hire request](https://github.com/ShashwatBuilds/shash.builds/issues/new?template=hire.yml) with your business name and current site. Keep phone numbers and emails out of it: issues are public. I'll reply there.

## Follow the build

[Instagram](https://www.instagram.com/shash.builds) &nbsp;|&nbsp;
[YouTube](https://www.youtube.com/@shash.builds) &nbsp;|&nbsp;
[LinkedIn](https://www.linkedin.com/in/shashbuilds) &nbsp;|&nbsp;
[X](https://x.com/shashbuilds)

Star the repo to get each new drop in your GitHub feed.

## Contributing

Found a bug, want a skill, or made something better? Read [CONTRIBUTING.md](CONTRIBUTING.md). Be decent: [Code of Conduct](CODE_OF_CONDUCT.md).

## License

- **Code** (skills, tools, templates, scripts): [MIT](LICENSE).
- **Content** (everything in `content/` and `media/`): [CC BY 4.0](LICENSE-CONTENT.md). Credit "shash.builds by Shashwat Jain".
- **Fonts** in the media kit: Bricolage Grotesque and Onest, both SIL Open Font License 1.1. Credits in [media/README.md](media/README.md).
