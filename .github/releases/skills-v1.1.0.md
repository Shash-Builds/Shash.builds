## shash.builds skills 1.1.0

**New: Niche Research.** Researches a content niche and turns it into a posting plan: top accounts, the best posts of the last 90 days and why they worked, audience questions and pain points, content gaps, 50 ranked video topics with hooks, posting times in ET, and the hashtags and search terms people actually use. Every row has a source link and a date. Haiku helpers do the collecting, so it stays cheap.

See it run on this repo's own niche: https://github.com/ShashwatBuilds/shash.builds/blob/main/research/niche/shash-builds/report.md

**Claude Code:**

```
/plugin marketplace add ShashwatBuilds/shash.builds
/plugin install niche-research@shashbuilds
```

**claude.ai:** download `niche-research-skill.zip` below, turn on code execution, upload it as a custom skill.

### New
- Niche Research skill with five Haiku helpers (accounts, posts, voices, signals, verifier).
- `niche_ledger.py`: checks every row has a link and a date, keeps posts inside the 90-day window, merges helper files, samples rows to re-check, counts, ranks topics and writes the report.
- `suggest.py`: real YouTube and Google search suggestions into the terms table.
- `youtube_read.cjs`: exact upload dates and views from public YouTube pages.
- The Master Skill's Marketing head now runs Niche Research before a new content plan.

Guide: https://github.com/ShashwatBuilds/shash.builds/tree/main/skills

---

Free and open source by shash.builds. Need a one-page website for your service business?
$400 flat, live in 7 days: https://github.com/ShashwatBuilds/shash.builds#hire-me
