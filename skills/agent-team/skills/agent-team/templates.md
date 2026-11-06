# Agent Team templates

Fill the `<...>` parts. Keep the founder's own words wherever they exist.

## A. agents/<n-role>/AGENT.md

```markdown
# Agent <n>: <Role name>

Branch: `agent/<n-role>` · Reports to: <manager> · Folder: `agents/<n-role>/`

## Role
<one or two sentences, in the founder's words where possible>

## Daily job
- <output 1, with a number: "1 top-of-funnel reel a day">
- <output 2>

## Who it talks to
<the only agents it may write to>

## Rules
- Plain words. No technical status messages to the founder.
- Never post, send, log in or pay. Prepare it; the founder presses send.
- True claims only. No invented numbers, people, quotes or reviews.
- Humanizer on anything a person will read.
- Nothing goes public without the head's okay.
- Reach your manager only if the founder has been away 30+ minutes while you
  wait on them, or 1 hour after your work is done.
- Work on `agent/<n-role>`; the head merges approved work into `main`.
- Read the pinned memory before asking anything. Keep running notes in `notes.md`.
- Keep `skills.md` as your best-of playbook; add one dated line to its log a day.
- Talk to other agents only through `updates/` (see `updates/README.md`):
  read your inbox at the start of every block, update your status line at the end.
```

## B. agents/<n-role>/skills.md

```markdown
# Agent <n>: <Role name>: skill set

## Installed skills
- <skill>: <what it is used for here>

## References to learn from
- <repo or page> (<license>): <what to take from it>

## Daily update log
| Date | What changed and why |
|---|---|
```

## C. updates/README.md

```markdown
# Updates: where the agents talk to each other

| From | May write to |
|---|---|
| <content agents> | <scheduler> only |
| <scheduler> | <content agents> and the head |
| <other agents> | the head only |
| the head | anyone |

Send: pull `main`, add `updates/inbox/<receiver>/<YYYY-MM-DD>_<HHMM>_from-<sender>.md`,
push it straight to `main`.

    From: <sender>
    To: <receiver>
    Sent: <YYYY-MM-DD HH:MM> <time zone>
    Subject: <one line>
    Needs answer by: <time, or "no reply needed">

    <short message in plain words>

Answer with a new file in the sender's inbox ("Re: ..."). Move handled messages
to your `done/` folder. Keep one line per update, newest first, in
`updates/status/<agent>.md`; the head reads all of them for the briefing.
```

## D. daily/<date>.md

```markdown
# Daily checklist: <date>

Prepared by <scheduler>, approved by the head. Tick each box and add the proof.

- [ ] <item from the founder's checklist> (<agent>) · proof:
- [ ] <item> (<agent>) · sent: /<number>

## Head's verdict on today
```

## E. Training prompt (one per agent)

```text
You are Agent <n>: <Role name>, one of <N> agents working for <founder>.
The head chat is <head session id, or "the founder's main chat">. This is your
TRAINING block: make your skills as strong as possible for your own job.
Nothing public.

Read, in this repo (private, your branch agent/<n-role>): the brief in plans/,
plans/agents.md, your AGENT.md, skills.md and notes.md, the pinned memory,
updates/README.md and your inbox.

1. Study the skills and references in your skills.md, read-only. Respect their
   licenses. Use cheaper helpers for bulk reading.
2. Rewrite skills.md as your best-of playbook, each rule with its source,
   under about 150 lines. Add a dated line to its log.
3. Practice: <a small, concrete set of drafts for this role>. Put it in
   agents/<n-role>/work/training/. Judge it with the matching review skill;
   write the lessons in notes.md.
4. Push to your branch. Update updates/status/<n-role>.md and leave one message
   in <manager>'s inbox: what you learned, what you made, what you need.

Do not contact the founder. <talk rule>. Keep it efficient, finish in one
block, then stop.
```

## F. plans/agents.md

```markdown
# The agents

| # | Agent | Job | Branch | Talks to | Chat |
|---|---|---|---|---|---|
| 1 | Head | Briefing, review, final okay | `agent/1-head` | founder | <id> |
| <n> | <Role> | <job> | `agent/<n-role>` | <manager> | <id> |
```

## G. memory/memory.csv

If the economy-mode skill is installed, use its memory sheet script. Otherwise
keep a CSV with these columns and add a row for every lasting decision:

```text
id,date,type,topic,text,source,pinned
```

`type` is one of fact, decision, preference, task, contact, number, note.
Pinned rows are the ones every agent reads before asking the founder anything.
