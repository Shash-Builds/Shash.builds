---
name: mock-builder
description: Build a one-page website mock for a local service business as one HTML file (name, trade, city; optional public logo, color, phone), with a shareable preview path. Placeholders are marked sample; never fake reviews. Use for "mock up a site for", "make a preview for this business".
---

# Mock Builder

Make a one-page mock a business owner can open on a phone, as a single HTML file.

## 1. Gather only public facts

Name, trade, city and state are enough. If the business has a public website, you may take
its logo URL, its main brand color and its public phone number from it. Nothing else about
the business goes on the page.

## 2. Build

```
python3 ${CLAUDE_SKILL_DIR}/scripts/mock.py --name "<name>" --trade "<trade>" --city "<city>" --state <ST> \
  [--color "#hex"] [--logo <url>] [--phone "<public number>"] [--by "<your name>"] --out previews/<slug>/index.html
```

(`scripts/mock.py` and `templates/style.css` are next to this SKILL.md.) The file has the
CSS inside it, so it works anywhere.

## 3. Rules

- The banner says it is a sample mock and not a claim about the business. Keep it.
- No reviews, ratings, years in business, licenses or awards unless the user gives you the
  business's own public source. The reviews panel says real reviews go there.
- If a site-audit JSON exists, make sure the mock fixes its top problems (call button, phone
  layout, service area) and tell the user which ones it fixes.

## 4. Share

Put every mock in one static site as `previews/<slug>/index.html` (Netlify drop or GitHub
Pages) and share `https://<site>/previews/<slug>/`. The page has `noindex` so search engines
skip it. Hand the link to `cold-email-drafter`.
