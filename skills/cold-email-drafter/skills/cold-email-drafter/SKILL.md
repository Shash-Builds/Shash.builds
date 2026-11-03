---
name: cold-email-drafter
description: Write a short cold email sequence to a local business from a site-audit result and a mock link: first email of 90 words or fewer plus day 3 and day 7 follow-ups, plain text, human tone, CAN-SPAM basics, checked by a script. Use for "write the cold email", "outreach email for this lead".
---

# Cold Email Drafter

Three short, honest emails a business owner might actually answer.

## 1. Inputs

- The site-audit JSON for the business (or its top problem).
- The mock link.
- The sender's real name and postal address (CAN-SPAM needs both).
- The owner's first name only if it is public (their own site or Google profile).

## 2. Draft

```
python3 ${CLAUDE_SKILL_DIR}/scripts/email_tool.py draft --audit audit.json --mock <link> \
  --sender "<real name>" --business "<business>" [--owner <first name>] [--city <city>] > emails.txt
```

(`scripts/email_tool.py` is next to this SKILL.md.) Then rewrite the personal line so it
sounds like a person who looked: one specific, provable thing from the audit, in plain
words. Keep the rest short. The offer line stays: "Want it live in 7 days for $400?" unless
the user's offer differs.

## 3. Rules

- Email 1: subject, greeting, one personal line, the mock link, the soft question, sign-off.
  90 words or fewer, not counting the address and opt-out lines.
- Follow-ups on day 3 and day 7, shorter, no guilt. Send them as replies in the same
  thread, so the "Re:" subject is true. Never put "Re:" on a new email.
- The email plainly says it is a business offer (the price line does this). Keep it.
- Plain text. One link. No attachments, no images, no tracking pixels.
- No em dashes, no hype, no fake familiarity, no claims about results.
- Every email ends with the sender's name, a real postal address and a one-line opt-out.
  Honor every opt-out.
- Run the humanizer on the personal line if it is installed.

## 4. Check before sending

```
python3 ${CLAUDE_SKILL_DIR}/scripts/email_tool.py check emails.txt
```

Fix everything it reports. It reminds you to fill the postal address placeholder.
