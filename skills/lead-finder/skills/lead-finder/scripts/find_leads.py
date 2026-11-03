#!/usr/bin/env python3
"""Lead finder: US service businesses by trade and city, from public sources, each run
through site-audit. Writes a CSV. The CSV is yours: keep it private, never commit it.

    python3 find_leads.py --trade plumber --city "Austin, TX" --out leads/austin-plumbers.leads.csv
    python3 find_leads.py --trade roofer --city "Tulsa, OK" --limit 20 --no-audit
    python3 find_leads.py --trade hvac --city "Boise, ID" --source places   # needs GOOGLE_PLACES_API_KEY

Sources:
  osm     (default) OpenStreetMap through Nominatim (to find the city) and Overpass (to find
          businesses). Free, no key, open data (ODbL: credit "© OpenStreetMap contributors").
          Coverage of small businesses varies by city.
  places  Google Places API (Text Search), with your own key in GOOGLE_PLACES_API_KEY. Paid by
          Google's pricing after any free credit. Follow Google's terms for storing results.
Never scrapes Google Maps or any site that forbids it. Audits fetch robots.txt and one page
per business (see site-audit).
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = "shashbuilds-lead-finder/1.0 (+https://github.com/ShashwatBuilds/shash.builds/tree/main/skills/lead-finder)"
OVERPASS = "https://overpass-api.de/api/interpreter"
NOMINATIM = "https://nominatim.openstreetmap.org/search"

# trade -> OSM tag filters (key, value)
TRADES = {
    "plumber": [("craft", "plumber")],
    "hvac": [("craft", "hvac"), ("craft", "heating_engineer")],
    "electrician": [("craft", "electrician")],
    "roofer": [("craft", "roofer")],
    "cleaner": [("craft", "cleaning"), ("office", "cleaning"), ("shop", "cleaning")],
    "landscaper": [("craft", "gardener"), ("craft", "landscaper"), ("shop", "garden_centre")],
    "painter": [("craft", "painter")],
    "carpenter": [("craft", "carpenter")],
    "handyman": [("craft", "handyman")],
    "locksmith": [("craft", "locksmith"), ("shop", "locksmith")],
    "pest control": [("craft", "pest_control"), ("shop", "pest_control")],
    "salon": [("shop", "hairdresser"), ("shop", "beauty")],
    "barber": [("shop", "hairdresser")],
    "dentist": [("amenity", "dentist"), ("healthcare", "dentist")],
    "auto repair": [("shop", "car_repair")],
    "car wash": [("amenity", "car_wash")],
    "pet grooming": [("shop", "pet_grooming")],
    "flooring": [("shop", "flooring"), ("craft", "floorer")],
}
FIELDS = ["business", "trade", "city", "website", "contact", "score", "problem_1", "problem_2", "problem_3", "source"]


def get_json(url, data=None, headers=None):
    h = {"User-Agent": UA}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read().decode("utf-8"))


def osm(trade, city, limit):
    q = urllib.parse.urlencode({"q": f"{city}, USA", "format": "json", "limit": 1, "countrycodes": "us"})
    places = get_json(f"{NOMINATIM}?{q}")
    if not places:
        sys.exit(f"Could not find {city!r} on OpenStreetMap. Try 'City, ST'.")
    s, n, w, e = places[0]["boundingbox"]
    time.sleep(1)  # Nominatim policy: at most one request a second
    bbox = f"{s},{w},{n},{e}"
    parts = "".join(f'nwr["{k}"="{v}"]({bbox});' for k, v in TRADES[trade])
    query = f"[out:json][timeout:60];({parts});out tags center {limit * 3};"
    data = get_json(OVERPASS, data=urllib.parse.urlencode({"data": query}).encode())
    rows = []
    for el in data.get("elements", []):
        t = el.get("tags", {})
        name = t.get("name")
        if not name:
            continue
        site = t.get("website") or t.get("contact:website") or t.get("url") or ""
        email = t.get("email") or t.get("contact:email") or ""
        rows.append({"business": name, "trade": trade, "city": city, "website": site,
                     "contact": email or (site and "contact page on website") or "", "source": "OpenStreetMap"})
    seen, out = set(), []
    for r in rows:
        key = r["business"].lower()
        if key not in seen:
            seen.add(key)
            out.append(r)
    return out[:limit]


def places(trade, city, limit):
    key = os.environ.get("GOOGLE_PLACES_API_KEY")
    if not key:
        sys.exit("Set GOOGLE_PLACES_API_KEY to use --source places.")
    body = json.dumps({"textQuery": f"{trade} in {city}", "pageSize": min(limit, 20)}).encode()
    data = get_json("https://places.googleapis.com/v1/places:searchText", data=body, headers={
        "Content-Type": "application/json", "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "places.displayName,places.websiteUri"})
    return [{"business": p.get("displayName", {}).get("text", ""), "trade": trade, "city": city,
             "website": p.get("websiteUri", ""), "contact": p.get("websiteUri") and "contact page on website" or "",
             "source": "Google Places API"} for p in data.get("places", [])][:limit]


def main():
    ap = argparse.ArgumentParser(description="Find US service businesses and audit their websites.")
    ap.add_argument("--trade", required=True, help="one of: " + ", ".join(TRADES))
    ap.add_argument("--city", required=True, help='"City, ST", for example "Austin, TX"')
    ap.add_argument("--limit", type=int, default=25)
    ap.add_argument("--source", choices=["osm", "places"], default="osm")
    ap.add_argument("--out", help="CSV path; use a leads/ folder or a .leads.csv name so git ignores it")
    ap.add_argument("--no-audit", action="store_true", help="skip site-audit")
    a = ap.parse_args()
    trade = a.trade.lower()
    if a.source == "osm" and trade not in TRADES:
        sys.exit(f"Unknown trade {a.trade!r}. Use one of: {', '.join(TRADES)}")
    rows = osm(trade, a.city, a.limit) if a.source == "osm" else places(trade, a.city, a.limit)
    if not a.no_audit:
        sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", "site-audit", "skills", "site-audit", "scripts"))
        try:
            import audit
        except ImportError:
            sys.exit("site-audit not found next to lead-finder. Install it, or pass --no-audit.")
        for i, r in enumerate(rows, 1):
            if not r["website"]:
                # Missing from the source is not proof the business has no site. Say so; don't score it.
                r["score"], r["problem_1"] = "", f"No website listed on {r['source']}. Search for the business before assuming it has none."
                continue
            print(f"[{i}/{len(rows)}] auditing {r['business']}", file=sys.stderr)
            res = audit.audit(r["website"], r["business"])
            r["score"] = "" if res.get("skipped") else res["score"]
            for j in range(3):
                r[f"problem_{j+1}"] = res["top_3"][j] if j < len(res["top_3"]) else ("skipped: " + res["skipped"] if j == 0 and res.get("skipped") else "")
    rows.sort(key=lambda r: -r["score"] if isinstance(r.get("score"), int) else 1)  # weakest sites first
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    fh = open(a.out, "w", newline="", encoding="utf-8") if a.out else sys.stdout
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
    if a.out:
        fh.close()
        print(f"Wrote {len(rows)} businesses to {a.out}. Keep this file private.", file=sys.stderr)
    if a.source == "osm":
        print("Business data © OpenStreetMap contributors (ODbL).", file=sys.stderr)


if __name__ == "__main__":
    main()
