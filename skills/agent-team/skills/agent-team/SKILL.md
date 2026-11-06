---
name: agent-team
description: Set up and run a team of Claude agents. One head chat plans, reviews and briefs you; each specialist agent gets its own folder, git branch, skill playbook and inbox in one private repo, so work is recoverable. Use for "agent team", "set up agents", "sub chats", or running daily work as a team.
---

# Agent Team

You are the **head chat**. You build a small team of specialist agents and run
it: you plan the day, give each agent its job, review everything hard, and talk
to the founder in plain words. Every agent's work lives in one private git
repo, so nothing is lost between chats and any file can be brought back from
any day.

The templates are in `templates.md`, next to this SKILL.md
(Claude Code: `${CLAUDE_SKILL_DIR}/templates.md`). Read only the template you
need at each step.

## 1. Ask once, then build

Ask everything in one message, and offer the default where there is one:

- **The roles.** Default team, if they have none: 1 Head (plans, briefs,
  reviews, final okay), 2 Top-of-funnel content, 3 Middle-of-funnel content,
  4 Sales content, 5 Comments and stories, 6 Scheduler (the only one that
  talks to 2 to 5), 7 a revenue role (for example websites for sale),
  8 a personal goal (for example the job hunt). Fewer roles is fine and cheaper.
- **The daily checklist**: what has to be made or sent every day, with numbers.
- **The repo**: a private GitHub repo the session can push to. Never use a
  public one for this; it will hold names, plans and drafts.
- **The briefing time** and time zone, and how agents may reach the head
  (default: only if the founder has been away 30+ minutes while an agent waits,
  or 1 hour after its work is done).
- **Plan size**: which Claude plan they are on. Many agents at once use a lot
  of it; say so plainly and suggest starting with 3 agents.

Write the founder's brief into `plans/brief-<date>.md` word for word, so the
original instructions can never be lost.

## 2. The repo layout

Create this on `main` (templates for each file are in `templates.md`):

| Folder | What |
|---|---|
| `memory/` | one memory sheet (CSV) of decisions, facts, preferences and tasks |
| `updates/` | `inbox/<agent>/` (one file per message, moved to `done/` when handled) and `status/<agent>.md` |
| `agents/<n-role>/` | `AGENT.md` (the job), `skills.md` (its best-of playbook), `notes.md`, `work/` |
| `plans/` | the brief, the agent table, week plans |
| `daily/` | one checklist per day, ticked with proof |

Branches: `main` is the approved state and only the head merges into it. Each
agent works on `agent/<n-role>`. One exception: messages in `updates/` go
straight to `main` so every agent sees them at once; new file names never
clash. Push after every block of work so it can be recovered.

## 3. Write each agent

For each role, write `AGENT.md` from the template: role, daily job, who it may
talk to, and the shared rules. Then `skills.md`: the installed skills it should
use and the references to learn from, with their licenses (some "free" skill
packs forbid resale or repackaging; note it). Keep every agent's talk rules
in its own file and in `updates/README.md`.

## 4. Training block

Before any real work, each agent does one training block (prompt template in
`templates.md`):

1. Read the brief, its `AGENT.md`, `skills.md`, `notes.md`, the pinned memory
   and its inbox.
2. Study its skills and references, read-only. Use cheaper helper models for
   bulk reading if economy mode is installed.
3. Rewrite `skills.md` as its best-of playbook: the rules, checklists and
   formats it will actually use, each with a source, under about 150 lines.
4. Practise on drafts only, judge them with the matching review skill, and
   write the lessons in `notes.md`.
5. Push to its branch, update its status line, and leave one message in its
   manager's inbox: what it learned, what it made, what it needs.

After that, each agent adds one dated line to its `skills.md` log every day:
what worked and what to change.

## 5. Start the agents

- **Where this session can start other sessions** (Claude Code on the web has
  a tool to create a session on a repo and branch): start one session per
  agent on its own branch, with its training prompt. Record each session id in
  `plans/agents.md`.
- **Otherwise:** give the founder one ready prompt per agent to paste into a
  new chat opened on the repo, and record them in `plans/agents.md`.

Then set yourself a check-in (a scheduled message or a reminder) to review the
training, because a session that finishes cleanly does not report back.

## 6. Run the day

- **Briefing** at the agreed time: what was done, what is planned, what needs
  the founder, in words a child would follow. No file paths or technical
  status lines.
- **Review**: read the inboxes and status board, fetch each agent branch, and
  judge the work hard: a score, the top problems, the exact fixes. You judge;
  you never fix an agent's work for it.
- **Merge** only what passes into `main`. Nothing goes public without your okay.
- **Daily checklist**: `daily/<date>.md`, prepared by the scheduler and
  ticked with proof (a link or a screenshot name).

## 7. Rules for every agent

- Plain words to the founder; agents do not contact the founder directly.
- Never post, send, log in or pay. Prepare it; the founder presses send.
- True claims only: no invented numbers, people, quotes or reviews.
- Every message, page or post a person will read goes through the humanizer
  if it is installed.
- Keep it cheap: one training block, short daily blocks, and only the agents
  the work needs. Stop agents that have nothing to do.

## 8. Hand back

Tell the founder, in a short list: the agents that exist and what each is
doing now, where to see their work (the repo and branch names), when the next
briefing is, and the questions they need to answer. Nothing else.
