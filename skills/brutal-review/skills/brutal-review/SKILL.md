---
name: brutal-review
description: Get a blunt, structured critique of a plan, pitch, resume or code from a different AI model (OpenAI, xAI, Anthropic, Google, local Ollama or the claude CLI). Returns a verdict, a score out of 100, ranked weaknesses with fixes, and the likeliest reason it fails. Use for "brutal review", "second opinion", "tear this apart".
---

# Brutal Review

A second opinion from a different model, shown word for word. A model reviewing its own
work goes easy on it; another model has other blind spots.

## 1. Before the first send (once per session)

Say which provider will get the text, and that emails, phone numbers and keys are removed
first. Ask once: "OK to send this to <provider>?" If the user says no, stop. Never ask for a
key in chat: keys come only from `OPENAI_API_KEY`, `XAI_API_KEY`, `ANTHROPIC_API_KEY` or
`GOOGLE_API_KEY` in the environment.

## 2. Pick a style

Ask if the user didn't say: `devil` (devil's advocate: the strongest case against),
`redteam` (how it breaks and who exploits it), or `headchef` (short, surgical, no
softening; the default).

## 3. Run it

Save the thing to review as a text file if it isn't one, then:

```
python3 ${CLAUDE_SKILL_DIR}/scripts/review.py <file> --style headchef [--context notes.md] [--provider openai] [--model <name>] [--second-pass] --md review.md
```

(`scripts/review.py` is next to this SKILL.md.) With no `--provider`, the first key found
wins; with none, it uses the `claude` CLI and says so: that is the same model family, so
tell the user it's a weaker second opinion. `--dry-run` shows exactly what would be sent.
`--second-pass` asks the reviewer to drop its weak points and add missed ones.

## 4. Show the result

Show the critique word for word: verdict, score, weaknesses (critical, major, minor, each
with its fix) and the 6-month failure reason. Never write or soften critique yourself,
and never fill in if the script fails: report its error message.

After the critique you may add your own view, under a heading that says it's yours
("Claude's take"). Keep it short and say where you disagree.

## 5. Next

Offer to fix the critical items first. Other reviews: Harsh Buyer Review is a buyer's
view of a product with competitor research; Careful Mode is Claude checking its own work.
This skill is an outside model's view of plans, pitches, resumes and code.
