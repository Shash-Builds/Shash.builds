#!/usr/bin/env python3
"""What people actually type: YouTube and Google search suggestions into terms.csv.

  python3 suggest.py FOLDER "claude skills" "one page website" ...
  python3 suggest.py FOLDER --where youtube,google "website for dentists"

For each seed phrase it asks the public autocomplete service (the one the
search box uses, no login, one request per second) and appends every
suggestion to FOLDER/terms.csv as kind "search", with the request URL as
source_url and today's date. Existing terms are skipped. Standard library only.
"""
import csv
import datetime as dt
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

COLS = ["id", "term", "kind", "platform", "evidence", "source_url", "checked"]
WHERE = {"youtube": "&ds=yt", "google": ""}


def suggestions(seed, where):
    url = ("https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us"
           f"{WHERE[where]}&q={urllib.parse.quote(seed)}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (niche-research)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.loads(r.read().decode("utf-8", errors="replace"))
    return url, [s for s in data[1] if isinstance(s, str)]


def main(argv):
    args = argv[1:]
    where = ["youtube", "google"]
    if "--where" in args:
        i = args.index("--where")
        if i + 1 >= len(args):
            print("--where needs a value, for example youtube,google")
            return 2
        where = [w.strip() for w in args[i + 1].split(",") if w.strip()]
        del args[i:i + 2]
        bad = [w for w in where if w not in WHERE]
        if bad:
            print(f"unknown --where {', '.join(bad)}; use youtube and/or google")
            return 2
    if len(args) < 2:
        print(__doc__.strip())
        return 2
    folder, seeds = pathlib.Path(args[0]), [s.strip() for s in args[1:] if s.strip()]
    path = folder / "terms.csv"
    if not path.exists():
        print(f"{path}: not found; run niche_ledger.py init first")
        return 1
    try:
        rows = list(csv.DictReader(path.read_text(encoding="utf-8-sig", errors="replace").splitlines()))
    except csv.Error as e:
        print(f"{path}: can't read it ({e})")
        return 1
    have = {(r.get("platform", ""), (r.get("term") or "").lower()) for r in rows}
    nums = [int(r["id"][2:]) for r in rows if (r.get("id") or "").startswith("t-") and r["id"][2:].isdigit()]
    n = max(nums, default=0)
    today = dt.date.today().isoformat()
    added, failed = [], []
    for seed in seeds:
        for w in where:
            try:
                url, found = suggestions(seed, w)
            except Exception as e:  # network, block or bad reply: say so and go on
                failed.append(f"{w} '{seed}': {type(e).__name__}")
                continue
            for pos, term in enumerate(found, 1):
                if (w, term.lower()) in have:
                    continue
                have.add((w, term.lower()))
                n += 1
                added.append({"id": f"t-{n:03}", "term": term, "kind": "search", "platform": w,
                              "evidence": f"{w} search suggestion {pos} for '{seed}' (US, English)",
                              "source_url": url, "checked": today})
            time.sleep(1)
    if added:
        with open(path, "a", newline="", encoding="utf-8") as fh:
            csv.DictWriter(fh, COLS).writerows(added)
    print(f"added {len(added)} terms to {path}")
    if failed:
        print("could not reach: " + "; ".join(failed))
    return 0 if added or not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
