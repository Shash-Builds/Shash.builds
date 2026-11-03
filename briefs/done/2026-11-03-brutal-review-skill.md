> **Result (2026-11-04):** shipped as [`skills/brutal-review`](../../skills/brutal-review), written from scratch (idea credited, nothing copied).
> Providers: OpenAI, xAI, Anthropic, Google, Ollama, claude CLI; keys from the environment only; emails, phones and keys removed before sending; validated JSON; Review head route.
> Tests: fake-provider test in run_tests.py and hostile inputs in chaos.py, no network or keys needed. Name kept as Brutal Review; the head chef style has no celebrity name.

# Brief: Brutal Review skill (outside-model critique)

From: the job-search chat, 2026-11-03. For: the head chat.

## The job

Build an original shash.builds skill that sends a plan, idea, pitch, resume or code to a
**different model** and returns a blunt, structured critique. Make it production ready and
ship it like every other tool (CLAUDE.md, "Adding or changing a tool", steps 1 to 8).

The idea comes from [zaripych/skills-brutal](https://github.com/zaripych/skills-brutal).
That repo has **no license**, so none of its code, prompts or wording may be copied here.
Write everything from scratch. Credit the idea in the skill's README ("Inspired by
zaripych/skills-brutal"). If its author later adds an open license, we can revisit.

## Why

A model reviewing its own work is biased toward it. An outside model has different
blind spots. Shashwat used the upstream tool on 2026-11-03 to review a plan (OpenAI,
"Gordon Ramsay" style); it scored 42/100 and found real holes that the plan's author
(Claude) had missed. That run's content is private and stays out of this repo.

## What it must do

1. **Take the thing to review** from the chat, a file, or pasted text, plus optional
   context files (code, docs).
2. **Pick a style:** devil's advocate, red team, or "head chef" (surgical, no mercy).
   Ask if not given. Use our own names and prompt text.
3. **Pick a model:** OpenAI, xAI, Anthropic, Google, a local Ollama, or the `claude`
   CLI. Keys only from environment variables (`OPENAI_API_KEY`, `XAI_API_KEY`,
   `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`); never ask for a key in chat, never log it.
   Default to whichever key is present; with none, fall back to the `claude` CLI and say
   it is the same model family.
4. **Return a fixed structure:** one-line verdict, score 1 to 100 (most land 30 to 60),
   weaknesses ranked critical, major, minor, each with a concrete fix, and the single most
   likely reason it fails in 6 months. Optional second pass where the reviewer drops its
   weak points and adds missed ones.
5. **Show the critique word for word.** Claude never writes critique itself or fills in
   when the script fails; it reports the error. After the critique, Claude may add its
   own take, clearly labelled as Claude's.
6. **Privacy first:** before sending anything to an outside provider, say which provider
   gets it, and strip emails, phone numbers and keys from the text (a script step, with a
   test). Ask once per session before the first send.

## Production checklist

- [ ] `skills/brutal-review/` plugin (or a better name), MIT `LICENSE.md`, plugin.json,
      marketplace entry, pointer in `.claude/skills/`, README row and install line.
- [ ] SKILL.md frontmatter `name` and `description` only, 55 words or fewer.
- [ ] One script (Python, stdlib plus `httpx` or the official SDKs; no Instructor
      unless needed), structured JSON output validated before printing, timeouts, retries
      on 429 and 5xx, plain error messages, never a traceback.
- [ ] Tests in `tests/run_tests.py` with a fake provider (no network, no key needed in
      CI); hostile inputs in `tests/chaos.py` (empty, binary, huge, cp1252, missing key,
      provider returns junk JSON, timeout).
- [ ] Master Skill: add to the registry and the **Review** head. Say how it differs from
      Harsh Buyer Review (buyer's view of a product, with competitor research) and Careful
      Mode (Claude checking its own work): this one is a second opinion from another model
      on plans, pitches, resumes and code. Rebuild `dist/master-full.md`.
- [ ] Zip for claude.ai in `scripts/build_skill_zip.py` if it can work there.
- [ ] `claude plugin validate .`, `python3 scripts/check.py`, full `tests/run_tests.py`
      with 0 failed. Then a STATUS.md entry.

## Open questions for Shashwat

- Name: "Brutal Review", "Second Opinion", or something else?
- Should the head chef style keep a celebrity reference? (Probably not: no real
  person's name in a public tool.)
