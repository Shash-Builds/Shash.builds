---
name: niche-research
description: Researches a content niche into a posting plan: top accounts, best posts of the last 90 days and why they worked, audience questions and pains, content gaps, ranked video topics with hooks, posting times in ET and real hashtags. Every row sourced and dated, run by Haiku helpers. Analysis only.
---

The files this skill uses sit next to this SKILL.md. In Claude Code that
folder is `${CLAUDE_SKILL_DIR}`; anywhere else, use the folder this file was
loaded from. Below, `SKILL_DIR` means that folder. When you pass it to a
helper, pass the full absolute path.

The method is in `SKILL_DIR/niche-research.md`. Inputs: the niche, the
audiences, the platforms and the goal. Output: `research/niche/<slug>/` in
the user's project. This skill is analysis only: never write posts here.

## With helpers (Claude Code, plugin installed): you only coordinate

Keep the main conversation cheap. Don't fetch pages yourself; the helpers
do that on Haiku and send back short summaries.

1. Print only what you need:
   `python3 "SKILL_DIR/scripts/read_sections.py" "SKILL_DIR/niche-research.md" 1 2 3 step1 9`.
   Search the project's memory sheet (if it has one) before asking the
   user anything. Run `python3 "SKILL_DIR/scripts/niche_ledger.py" init <folder>`
   and fill in `brief.md`.
2. Start these Haiku helpers in parallel, each with SKILL_DIR and the
   folder: `niche-accounts`, `niche-voices` (one per audience, each writing
   `voices-<audience>.csv`) and `niche-signals`. When `niche-accounts` is
   done, start `niche-posts`. Installed as a plugin, their names start with
   `niche-research:`.
3. Run `niche_ledger.py merge`, then start `niche-verifier`. Send any table
   with more than 1 in 10 fixes back to its helper.
4. Print step 7 (`read_sections.py ... step7 step8 step9 step10`), run
   `tables`, and write `gaps.csv` and `topics.csv` yourself from
   `tables.md` and the CSVs: this is judgement, so it stays with you. Then
   `rank`, `check` until it passes, `report`, and write the summary at the
   top of `report.md`.
5. Hand off as step 10 says. The social-media skill can turn `topics.csv`
   into a calendar and the linkedin skill can draft the LinkedIn posts.

If a helper isn't available under either name, do its steps yourself, one
table at a time.

## Without helpers (claude.ai or any chat)

Follow `SKILL_DIR/niche-research.md` from step 1 to step 10 yourself, in
order, one table at a time. Choosing Haiku as the model keeps it cheap.

## Tools

- `SKILL_DIR/scripts/niche_ledger.py`: init, check, merge, sample, tables,
  rank and report (needs only Python 3).
- `SKILL_DIR/scripts/read_sections.py`: prints only the sections of the
  method a step needs (`--list` shows them).
