---
name: lead-finder
description: Find service businesses (plumbers, roofers, HVAC, cleaners, salons, dentists and more) by trade and city from public sources (OpenStreetMap, or Google Places with your key), audit each site, and write a private CSV ranked weakest first. Use for "find leads", "prospects in <city>".
---

# Lead Finder

Find local service businesses from sources that allow it, audit each website, and hand
back a CSV ranked weakest site first. The list belongs to the user: never commit it, never
publish it.

## 1. Run it

```
python3 ${CLAUDE_SKILL_DIR}/scripts/find_leads.py --trade plumber --city "Austin, TX" --limit 25 --out leads/austin-plumbers.leads.csv
```

(`scripts/find_leads.py` is next to this SKILL.md.) Trades: plumber, hvac, electrician,
roofer, cleaner, landscaper, painter, carpenter, handyman, locksmith, pest control, salon,
barber, dentist, auto repair, car wash, pet grooming, flooring.

- Default source: OpenStreetMap (Nominatim finds the city, Overpass finds businesses). Free,
  no key. Credit "© OpenStreetMap contributors". Coverage varies by city. The city lookup
  is currently limited to US cities.
- `--source places`: Google Places API with the user's own `GOOGLE_PLACES_API_KEY`. Google
  bills for it; follow Google's terms on storing results.
- Never scrape Google Maps or any site whose terms forbid it.

The audit needs the `site-audit` skill installed next to this one (or pass `--no-audit`).

## 2. Read the CSV

Columns: business, trade, city, website, contact, score, problem_1..3, source. A blank
website means the source didn't list one, which is not proof there is none: say so and
suggest a quick search before calling it "no website". `contact` is a public email from the
source or "contact page on website".

## 3. Keep it private

Save under `leads/` or as `*.leads.csv` and make sure `.gitignore` covers both. Remind the
user that cold email needs CAN-SPAM basics (see `cold-email-drafter`).

## 4. Hand-offs

Pick the weakest sites, then `mock-builder` for each and `cold-email-drafter` for the emails.
