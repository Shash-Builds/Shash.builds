# Power: Dashboard

For a personal dashboard that tracks what the user cares about: goals, job hunt, content, money, habits,
to-dos. Their own files, one page, kept up to date by every session.

## Set it up (once)
1. **Ask what to track** in one short message with sensible suggestions from what you know about them
   (memory sheet, current projects). For each thing: its name, a target, the unit, the period (day, week,
   month or all) and whether entries add up (applications sent) or the latest counts (followers, weight).
2. **Give it its own chat.** Offer to start a separate "Dashboard" chat so updates don't clutter the work:
   - Claude Code cloud with session tools: create the session with a handover prompt (what is tracked,
     where the files live, how to update), after the user's yes.
   - Anywhere else: give the user a ready prompt in ONE code block to paste into a new chat.
3. **Create it** with `scripts/dashboard.py` next to the super-mode SKILL.md
   (`${CLAUDE_SKILL_DIR}/scripts/dashboard.py`):
   `python3 dashboard.py init --dir dashboard --title "<their name>'s dashboard" --track "Applications sent:50:emails:month:sum" ...`
   then `build`, and show the page. Two looks: `--theme glass` (Apple-style frosted glass, light and dark,
   the default) or `--theme jarvis` (dark HUD with glowing gauges); ask which they want. Each card has a
   Details button that opens a full page for that area (totals, average, best day, streak, 30-day chart,
   every entry); the main screen stays a simple overview. On claude.ai, build the same page as an artifact from their data.

## Keep it current (every session)
- When something tracked happens in any chat (an application sent, a post published, a payment, a habit
  done), log it: `dashboard.py log --dir dashboard "<metric>" <value> --note "<what>"`.
- New to-dos and deadlines: `dashboard.py todo --dir dashboard "<item>" --due YYYY-MM-DD`; close with `--done`.
- Rebuild after changes (`build`) and give the one-line summary from `show` when the user asks how things
  are going.
- Change what is tracked only when the user asks; edit `config.json`, never the history in `log.csv`.

## Rules
Real numbers only, each with a source (a log line, a report, the user). The data stays in the user's folder;
nothing is uploaded or shared unless they ask.

## Done when
The user chose what to track, the dashboard builds and opens, and the dashboard chat (or prompt) is set up.
