# AGENTS.md

A guide for AI agents (Claude, Codex, Cursor and others) working with this repo.

## Find things

- `catalog.json` lists every skill and tool: `name`, `kind`, `path`, `summary`, `version`, `install`.
- `llms.txt` is the same index in plain text with links.
- Each item's folder has a `README.md` in one fixed layout: what it does, install in 3 steps, before and after, examples, FAQ, changelog.

## Install a skill for a user

1. Read the skill's `README.md` and `SKILL.md`.
2. Claude Code: copy `skills/<name>/` to `~/.claude/skills/<name>/` (or the project's `.claude/skills/`).
3. Claude.ai: the user uploads `<name>.zip` from the matching GitHub Release in Settings, Capabilities, Skills.

## Contribute

- Read `CONTRIBUTING.md`. Run `python3 scripts/check.py` before proposing a change.
- New item: copy `templates/ITEM-README.md`, make a header with `python3 media/build.py header "Name" --kind skill|tool --out <folder>/header.svg`, add a row to `catalog.json`.
- Never add keys, tokens, personal data, client data, or photos of people. The repo is public.
- Write plain US English. No em dashes. No invented numbers, users or reviews.

## Repo map

| Path | What |
| --- | --- |
| `skills/` | Claude skills |
| `tools/` | Web tools and one-page site starters |
| `templates/` | README, release and video templates |
| `content/` | Daily posts and video scripts (CC BY 4.0) |
| `media/` | Brand kit and its build script |
| `research/` | Sourced, dated research |
| `briefs/` | Jobs queued for the build, `briefs/done/` when shipped |
| `STATUS.md` | Build log and backlog |
