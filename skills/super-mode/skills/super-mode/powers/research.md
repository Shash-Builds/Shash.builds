# Power: Research

For competitors, markets, prices, companies, people's public work, tools, "is this real", any sourced answer.

## Builds on
**competitor-research** (`skills/competitor-research/skills/competitor-research/competitor-research.md`,
its Haiku helpers and `ledger.py`), **niche-research**, **harsh-buyer-review** for the buyer's view.

## Method (fan out, then check)
1. Write a one-paragraph brief: question, scope, dates, what "done" looks like. Confirm if it is big.
2. Split the work into 2 to 4 even slices (by source, region or question) and run cheap helpers in
   parallel. Each returns a fixed table with a source link, the quoted line and the date for every fact,
   and "not found" instead of a guess.
3. If helpers can't reach a site, fetch the pages yourself, save them as text and hand the files over.
   Respect blocks and logins: never get around them.
4. Merge, drop duplicates, spot-check rows against the source, compute every total in code.
5. Report: answer first in 3 lines, then the table, then what is unknown.

## Rules
Primary sources first (the company's own page, filings, official docs). Mark opinions and forum posts as
such. Dates on everything; flag anything older than the question allows.

## Done when
Every claim has a link and a date, numbers come from code, gaps are listed, the user got the answer first.
