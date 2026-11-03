#!/usr/bin/env python3
"""Ledger for shash.builds Niche Research: checks, counts, ranks and reports.

  python3 niche_ledger.py init   FOLDER   create the folder and every CSV header
  python3 niche_ledger.py check  FOLDER   list every broken rule, exit 1 if any
  python3 niche_ledger.py merge  FOLDER   fold part files (voices-a.csv, ...) into the main CSVs
  python3 niche_ledger.py sample FOLDER   about 1 in 5 rows per fact table to re-check
  python3 niche_ledger.py tables FOLDER   write tables.md (repeat counts, formats, hooks, terms)
  python3 niche_ledger.py rank   FOLDER   score and sort topics.csv (demand x gap x fit)
  python3 niche_ledger.py report FOLDER   write the sourced tables into report.md

Standard library only. Reads CSVs written by people and by models, so it
refuses bad input with a plain message instead of a traceback.
"""
import csv
import datetime as dt
import pathlib
import random
import re
import sys
from collections import Counter

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

TABLES = {
    "accounts": ("a", ["id", "name", "platform", "url", "audience", "followers", "followers_as_of", "cadence",
                       "formats", "why_relevant", "source_url", "checked"]),
    "posts": ("p", ["id", "platform", "url", "author", "posted", "metric", "metric_value", "hook_type", "format",
                    "length", "why_it_worked", "source_url", "checked"]),
    "voices": ("v", ["id", "kind", "text", "audience", "where", "quote", "posted", "source_url", "checked"]),
    "terms": ("t", ["id", "term", "kind", "platform", "evidence", "source_url", "checked"]),
    "times": ("h", ["id", "platform", "days", "slot_et", "evidence", "source_url", "checked"]),
    "gaps": ("g", ["id", "gap", "audience", "evidence", "why_open"]),
    "topics": ("k", ["id", "topic", "hook", "audience", "platform", "format", "demand", "gap", "fit", "evidence"]),
}
FACT_TABLES = ["accounts", "posts", "voices", "terms", "times"]
MINIMUM = {"full": {"accounts": 30, "posts": 20, "voices": 40, "topics": 50},
           "quick": {"accounts": 10, "posts": 10, "voices": 20, "topics": 20}}
GAP_WORDS = {"not found", "hidden", "blocked"}
WINDOW_DAYS = 90
csv.field_size_limit(10 * 1024 * 1024)


class Refuse(Exception):
    pass


def read(folder, name):
    path = folder / f"{name}.csv"
    table = name.split("-")[0]
    if not path.exists():
        return []
    try:
        text = path.read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError:
        text = path.read_bytes().decode("cp1252", errors="replace")
    if "\x00" in text:
        raise Refuse(f"{path.name}: contains null bytes; save it again as a plain CSV")
    lines = text.splitlines()
    if not lines:
        return []
    try:
        dialect = csv.Sniffer().sniff(lines[0], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.DictReader(lines, dialect=dialect))
    want = TABLES[table][1]
    have = [h.strip() for h in (csv.DictReader(lines[:1], dialect=dialect).fieldnames or [])]
    missing = [c for c in want if c not in have]
    if missing:
        raise Refuse(f"{path.name}: missing columns {', '.join(missing)}")
    return [{(k or "").strip(): (v if isinstance(v, str) else "").strip() for k, v in r.items()} for r in rows]


def write(folder, name, rows, cols):
    with open(folder / f"{name}.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def brief(folder):
    path = folder / "brief.md"
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    m = re.search(r"run_date:\s*(\d{4}-\d{2}-\d{2})", text)
    run = parse_date(m.group(1)) if m else None
    depth = "quick" if re.search(r"depth:\s*quick", text, re.I) else "full"
    return run, depth


def parse_date(s):
    try:
        return dt.date.fromisoformat(s)
    except (TypeError, ValueError):
        return None


def is_number(s):
    return bool(re.fullmatch(r"\d+(\.\d+)?", s))


def cmd_init(folder):
    folder.mkdir(parents=True, exist_ok=True)
    made = []
    for name, (_, cols) in TABLES.items():
        path = folder / f"{name}.csv"
        if not path.exists():
            write(folder, name, [], cols)
            made.append(path.name)
    b = folder / "brief.md"
    if not b.exists():
        b.write_text(f"# Brief\n\n- Niche:\n- Audiences:\n- Platforms:\n- Goal:\n"
                     f"- run_date: {dt.date.today().isoformat()}\n- depth: full\n", encoding="utf-8")
        made.append("brief.md")
    print(f"{folder}: created {', '.join(made) if made else 'nothing (all files exist)'}")


def problems(folder):
    out = []
    run, depth = brief(folder)
    today = dt.date.today()
    if run is None:
        out.append("brief.md: no 'run_date: YYYY-MM-DD' line")
    data = {name: read(folder, name) for name in TABLES}
    ids = set()
    for name, rows in data.items():
        prefix = TABLES[name][0]
        seen = set()
        for i, r in enumerate(rows, 2):
            rid = r.get("id", "")
            where = f"{name}.csv line {i} ({rid or 'no id'})"
            if not re.fullmatch(rf"{prefix}-\d{{3,}}", rid):
                out.append(f"{where}: id should look like {prefix}-001")
            if rid in seen:
                out.append(f"{where}: duplicate id")
            seen.add(rid)
            ids.add(rid)
            if name in FACT_TABLES:
                if not r.get("source_url", "").startswith(("http://", "https://")):
                    out.append(f"{where}: source_url must be a link (http...)")
                checked = parse_date(r.get("checked", ""))
                if checked is None:
                    out.append(f"{where}: checked must be a date YYYY-MM-DD")
                elif checked > today + dt.timedelta(days=1):
                    out.append(f"{where}: checked date is in the future")
    for i, r in enumerate(data["accounts"], 2):
        f = r["followers"]
        if f and f.lower() not in GAP_WORDS and not is_number(f):
            out.append(f"accounts.csv line {i} ({r['id']}): followers must be a plain number "
                       f"(12400, not 12,400 or 12.4K) or not found / hidden / blocked")
        if is_number(f) and parse_date(r["followers_as_of"]) is None:
            out.append(f"accounts.csv line {i} ({r['id']}): followers_as_of must be a date")
    for i, r in enumerate(data["posts"], 2):
        v = r["metric_value"]
        if v and v.lower() not in GAP_WORDS and not is_number(v):
            out.append(f"posts.csv line {i} ({r['id']}): metric_value must be a plain number")
        posted = parse_date(r["posted"])
        if posted is None:
            out.append(f"posts.csv line {i} ({r['id']}): posted must be a date (best posts need one)")
        elif run and not (run - dt.timedelta(days=WINDOW_DAYS) <= posted <= run):
            out.append(f"posts.csv line {i} ({r['id']}): posted {posted} is outside the 90 days before {run}")
    for i, r in enumerate(data["voices"], 2):
        if r["kind"] not in ("question", "pain"):
            out.append(f"voices.csv line {i} ({r['id']}): kind must be question or pain")
        if len(r["quote"]) > 200:
            out.append(f"voices.csv line {i} ({r['id']}): quote over 200 characters")
        if re.search(r"(^|\s)u/\w|@\w{2,}", r["quote"]):
            out.append(f"voices.csv line {i} ({r['id']}): quote names a person; keep only their words")
    for i, r in enumerate(data["terms"], 2):
        if r["kind"] not in ("hashtag", "search", "keyword"):
            out.append(f"terms.csv line {i} ({r['id']}): kind must be hashtag, search or keyword")
    for i, r in enumerate(data["times"], 2):
        if not re.fullmatch(r"\d{2}:\d{2}-\d{2}:\d{2}", r["slot_et"]):
            out.append(f"times.csv line {i} ({r['id']}): slot_et must look like 09:00-11:00")
    for name in ("gaps", "topics"):
        for i, r in enumerate(data[name], 2):
            ev = r["evidence"].split()
            if not ev:
                out.append(f"{name}.csv line {i} ({r['id']}): no evidence ids")
            for e in ev:
                if e not in ids:
                    out.append(f"{name}.csv line {i} ({r['id']}): evidence {e} is not a row id")
    for i, r in enumerate(data["topics"], 2):
        for c in ("demand", "gap", "fit"):
            if r[c] not in {"1", "2", "3", "4", "5"}:
                out.append(f"topics.csv line {i} ({r['id']}): {c} must be a whole number 1 to 5")
        if len(r["hook"].split()) > 12:
            out.append(f"topics.csv line {i} ({r['id']}): hook over 12 words")
    for name, n in MINIMUM[depth].items():
        if len(data[name]) < n:
            out.append(f"{name}.csv: {len(data[name])} rows, {depth} depth needs {n}")
    return out


def cmd_check(folder):
    found = problems(folder)
    if found:
        print("\n".join(found))
        print(f"\n{len(found)} problem(s).")
        return 1
    print("check passed")
    return 0


def cmd_merge(folder):
    done = []
    for name in TABLES:
        parts = sorted(p for p in folder.glob(f"{name}-*.csv"))
        if not parts:
            continue
        rows = read(folder, name)
        seen = {r["id"] for r in rows}
        for part in parts:
            for r in read(folder, part.stem):
                if r["id"] in seen:
                    raise Refuse(f"{part.name}: id {r['id']} is already in {name}.csv; give each helper its own ids")
                seen.add(r["id"])
                rows.append(r)
        write(folder, name, rows, TABLES[name][1])
        (folder / "parts").mkdir(exist_ok=True)
        for part in parts:
            part.replace(folder / "parts" / part.name)
        done.append(f"{name}.csv (+{len(parts)} part files)")
    print("merged " + ", ".join(done) if done else "no part files to merge")
    return 0


def cmd_sample(folder):
    rng = random.Random(7)
    for name in FACT_TABLES:
        rows = read(folder, name)
        if not rows:
            continue
        k = max(1, round(len(rows) / 5))
        for r in rng.sample(rows, min(k, len(rows))):
            print(f"{r['id']}\t{r['source_url']}")
    return 0


def md(s):
    return (s or "").replace("|", "\\|").replace("\n", " ")


def link(r):
    url = r.get("source_url", "")
    return f"[source]({url}) {r.get('checked', '')}" if url else "no source"


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def cmd_tables(folder):
    voices, posts, terms = read(folder, "voices"), read(folder, "posts"), read(folder, "terms")
    out = ["# Tables (computed by niche_ledger.py)", ""]
    out += ["## Repeated questions and pains", "", "| Kind | Text | Times seen | Rows |", "|---|---|---|---|"]
    groups = {}
    for r in voices:
        groups.setdefault((r["kind"], norm(r["text"])), []).append(r)
    for (kind, _), rows in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        out.append(f"| {kind} | {md(rows[0]['text'])} | {len(rows)} | {' '.join(x['id'] for x in rows)} |")
    for col, title in (("format", "Formats"), ("hook_type", "Hook types"), ("platform", "Platforms")):
        out += ["", f"## {title} among the best posts", "", f"| {title[:-1]} | Posts |", "|---|---|"]
        for value, n in Counter(r[col] or "not set" for r in posts).most_common():
            out.append(f"| {md(value)} | {n} |")
    out += ["", "## Terms by platform", "", "| Platform | Kind | Term | Rows |", "|---|---|---|---|"]
    tg = {}
    for r in terms:
        tg.setdefault((r["platform"], r["kind"], r["term"].lower()), []).append(r["id"])
    for (plat, kind, term), rid in sorted(tg.items(), key=lambda kv: (kv[0][0], -len(kv[1]), kv[0][2])):
        out.append(f"| {md(plat)} | {kind} | {md(term)} | {' '.join(rid)} |")
    (folder / "tables.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {folder / 'tables.md'}")
    return 0


def cmd_rank(folder):
    rows = read(folder, "topics")
    bad = [r["id"] for r in rows if any(r[c] not in {"1", "2", "3", "4", "5"} for c in ("demand", "gap", "fit"))]
    if bad:
        raise Refuse(f"topics.csv: demand, gap and fit must be 1 to 5 before ranking ({', '.join(bad[:5])})")
    for r in rows:
        r["score"] = str(int(r["demand"]) * int(r["gap"]) * int(r["fit"]))
    rows.sort(key=lambda r: (-int(r["score"]), -len(r["evidence"].split()), r["id"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = str(i)
    write(folder, "topics", rows, ["rank", "score"] + TABLES["topics"][1])
    print(f"ranked {len(rows)} topics; top: {rows[0]['topic'] if rows else 'none'}")
    return 0


MARK = "<!-- niche_ledger report: everything below is generated -->"


def cmd_report(folder):
    run, _ = brief(folder)
    acc, posts, voices = read(folder, "accounts"), read(folder, "posts"), read(folder, "voices")
    terms, times, gaps, topics = read(folder, "terms"), read(folder, "times"), read(folder, "gaps"), read(folder, "topics")
    if topics and "rank" in topics[0]:
        topics.sort(key=lambda r: int(r["rank"]) if r["rank"].isdigit() else 10 ** 6)
    out = [MARK, "", f"Run date: {run or 'not set'}. Every row links its source and the date it was checked.", ""]
    out += [f"## Accounts and creators ({len(acc)})", "",
            "| # | Name | Platform | Followers | Cadence | Formats | Why | Source |", "|---|---|---|---|---|---|---|---|"]
    for r in acc:
        f = f"{int(float(r['followers'])):,} ({r['followers_as_of']})" if is_number(r["followers"]) else r["followers"]
        out.append(f"| {r['id']} | [{md(r['name'])}]({r['url']}) | {md(r['platform'])} | {f} | {md(r['cadence'])} | "
                   f"{md(r['formats'])} | {md(r['why_relevant'])} | {link(r)} |")
    out += ["", f"## Best posts, last 90 days ({len(posts)})", "",
            "| # | Post | Posted | Metric | Hook | Format | Length | Why it worked | Source |",
            "|---|---|---|---|---|---|---|---|---|"]
    for r in posts:
        v = f"{int(float(r['metric_value'])):,}" if is_number(r["metric_value"]) else r["metric_value"]
        out.append(f"| {r['id']} | [{md(r['author'])}, {md(r['platform'])}]({r['url']}) | {r['posted']} | "
                   f"{v} {md(r['metric'])} | {md(r['hook_type'])} | {md(r['format'])} | {md(r['length'])} | "
                   f"{md(r['why_it_worked'])} | {link(r)} |")
    for kind, title in (("question", "Audience questions"), ("pain", "Pain points")):
        rows = [r for r in voices if r["kind"] == kind]
        out += ["", f"## {title} ({len(rows)})", "", "| # | What | Audience | Where | In their words | Source |",
                "|---|---|---|---|---|---|"]
        for r in rows:
            out.append(f"| {r['id']} | {md(r['text'])} | {md(r['audience'])} | {md(r['where'])} | "
                       f"\"{md(r['quote'])}\" | {link(r)} |")
    out += ["", f"## Content gaps ({len(gaps)})", "", "| # | Gap | Audience | Why it's open | Evidence |",
            "|---|---|---|---|---|"]
    for r in gaps:
        out.append(f"| {r['id']} | {md(r['gap'])} | {md(r['audience'])} | {md(r['why_open'])} | {r['evidence']} |")
    out += ["", f"## Video topics, ranked ({len(topics)})", "",
            "| Rank | Topic | Hook | Audience | Platform | Format | D x G x F | Evidence |",
            "|---|---|---|---|---|---|---|---|"]
    for r in topics:
        out.append(f"| {r.get('rank', '')} | {md(r['topic'])} | \"{md(r['hook'])}\" | {md(r['audience'])} | "
                   f"{md(r['platform'])} | {md(r['format'])} | {r['demand']}x{r['gap']}x{r['fit']} = "
                   f"{r.get('score', '')} | {r['evidence']} |")
    out += ["", "## Best posting times (US Eastern)", "", "| # | Platform | Days | Slot (ET) | Evidence | Source |",
            "|---|---|---|---|---|---|"]
    for r in times:
        out.append(f"| {r['id']} | {md(r['platform'])} | {md(r['days'])} | {r['slot_et']} | {md(r['evidence'])} | "
                   f"{link(r)} |")
    out += ["", f"## Hashtags and search terms ({len(terms)})", "", "| # | Term | Kind | Platform | Evidence | Source |",
            "|---|---|---|---|---|---|"]
    for r in terms:
        out.append(f"| {r['id']} | {md(r['term'])} | {r['kind']} | {md(r['platform'])} | {md(r['evidence'])} | "
                   f"{link(r)} |")
    path = folder / "report.md"
    head = path.read_text(encoding="utf-8", errors="replace").split(MARK)[0].rstrip() if path.exists() else \
        "# Niche research\n\n(Write the five-line answer, per-platform plan, what not to do and the data note here.)"
    path.write_text(head + "\n\n" + "\n".join(out) + "\n", encoding="utf-8")
    print(f"wrote {path}")
    return 0


COMMANDS = {"init": cmd_init, "check": cmd_check, "merge": cmd_merge, "sample": cmd_sample, "tables": cmd_tables, "rank": cmd_rank,
            "report": cmd_report}


def main(argv):
    if len(argv) != 3 or argv[1] not in COMMANDS:
        print(__doc__.strip())
        return 2
    folder = pathlib.Path(argv[2])
    if argv[1] != "init" and not folder.is_dir():
        print(f"{folder}: no such folder; run init first")
        return 1
    try:
        return COMMANDS[argv[1]](folder) or 0
    except Refuse as e:
        print(e)
        return 1
    except OSError as e:
        print(f"can't read or write: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
