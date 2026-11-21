"""A personal dashboard that tracks what the user cares about, in one self-contained HTML page.

The data lives in a folder the user owns (default ./dashboard): config.json (what to track), log.csv (every
entry) and todo.csv (open items). Nothing leaves the computer.

  python3 dashboard.py init  --dir dashboard --title "My dashboard" --track "Applications sent:50:count:month:sum" \
                             --track "Weight:72:kg:day:last"
  python3 dashboard.py log   --dir dashboard "Applications sent" 3 --note "RedBolt, Netr, SiaHealth" [--date 2026-11-21]
  python3 dashboard.py todo  --dir dashboard "Follow up with Sahaj" --due 2026-11-27     (add)  |  --done "Follow up"  (close)
  python3 dashboard.py build --dir dashboard [--out dashboard/index.html]
  python3 dashboard.py show  --dir dashboard            (plain-text summary for the chat)

--track is "name:target:unit:period:how". period = day, week, month or all. how = sum (add up entries, e.g.
applications) or last (latest value, e.g. weight or followers). Target and unit may be empty."""
import argparse
import csv
import datetime as dt
import html
import io
import json
import math
import re
import os
import sys
from pathlib import Path

PERIODS = {"day", "week", "month", "all"}
HOWS = {"sum", "last"}
THEMES = {"glass", "jarvis"}


def fail(msg: str) -> None:
    print(msg)
    sys.exit(2)


def read_text(p: Path) -> str:
    raw = p.read_bytes()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def number(v) -> float | None:
    try:
        x = float(str(v).replace(",", "").strip())
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def day(v: str) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(v).strip()[:10])
    except ValueError:
        return None


def load_config(d: Path) -> dict:
    p = d / "config.json"
    if not p.exists():
        fail(f"No dashboard in {d}. Start one with: python3 dashboard.py init --dir {d} --track \"Name:target:unit:period:sum\"")
    try:
        cfg = json.loads(read_text(p))
        assert isinstance(cfg, dict) and isinstance(cfg.get("track", []), list)
    except (ValueError, AssertionError):
        fail(f"{p} is not a valid dashboard config. Fix it or run init again in a new folder.")
    return cfg


def rows(p: Path) -> list:
    if not p.exists():
        return []
    text = read_text(p).replace("\x00", "")
    sample = text[:2000]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t") if sample.strip() else csv.excel
    except csv.Error:
        dialect = csv.excel
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    try:
        return [r for r in csv.DictReader(io.StringIO(text, newline=""), dialect=dialect)]
    except csv.Error:
        fail(f"{p} is not a readable CSV file. Restore it from a backup, or move it away to start a fresh log.")
    return []


def append(p: Path, header: list, row: list) -> None:
    new = not p.exists() or p.stat().st_size == 0
    with open(p, "a", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        if new:
            w.writerow(header)
        w.writerow(row)


def parse_track(spec: str) -> dict:
    parts = (spec.split(":") + ["", "", "", ""])[:5]
    name, target, unit, period, how = [x.strip() for x in parts]
    if not name:
        fail(f"--track {spec!r} needs a name, e.g. \"Applications sent:50:count:month:sum\"")
    period = period or "all"
    how = how or "sum"
    if period not in PERIODS or how not in HOWS:
        fail(f"--track {spec!r}: period must be day, week, month or all; how must be sum or last")
    t = number(target) if target else None
    return {"name": name, "target": t, "unit": unit, "period": period, "how": how}


def window_start(period: str, today: dt.date) -> dt.date | None:
    if period == "day":
        return today
    if period == "week":
        return today - dt.timedelta(days=today.weekday())
    if period == "month":
        return today.replace(day=1)
    return None


def summarise(cfg: dict, log: list, today: dt.date) -> list:
    out = []
    for t in cfg.get("track", []):
        if not isinstance(t, dict) or not t.get("name"):
            continue
        hist = sorted(((day(r.get("date")), number(r.get("value")), str(r.get("note") or "")) for r in log
                       if r.get("metric") == t["name"]), key=lambda e: (e[0] or dt.date.min))
        hist = [(d, v, n) for d, v, n in hist if d and v is not None]
        entries = [(d, v) for d, v, _ in hist]
        start = window_start(t.get("period", "all"), today)
        inside = [v for d, v in entries if (start is None or d >= start) and d <= today]
        how = t.get("how", "sum")
        now = (sum(inside) if how == "sum" else (inside[-1] if inside else None)) if inside else (0 if how == "sum" else None)
        target = number(t.get("target"))
        pct = None if (target in (None, 0) or now is None) else max(0.0, min(100.0, 100 * now / target))

        def per_day(dd):
            vals = [v for d, v in entries if d == dd]
            return (sum(vals) if how == "sum" else vals[-1]) if vals else None

        spark = [per_day(today - dt.timedelta(days=i)) for i in range(13, -1, -1)]
        month = [per_day(today - dt.timedelta(days=i)) for i in range(29, -1, -1)]
        days = sorted({d for d, _ in entries if d <= today})
        streak, cur = 0, today
        while cur in set(days):
            streak += 1
            cur -= dt.timedelta(days=1)
        daily = [x for x in (per_day(d) for d in days) if x is not None]
        stats = {"all": (sum(v for _, v in entries) if how == "sum" else (entries[-1][1] if entries else None)),
                 "avg": (sum(daily) / len(daily)) if daily else None,
                 "best": max(daily) if daily else None, "days": len(days), "streak": streak}
        slug = re.sub(r"[^a-z0-9]+", "-", t["name"].lower()).strip("-") or "metric"
        out.append({**t, "now": now, "pct": pct, "spark": spark, "month": month, "entries": len(entries),
                    "hist": hist, "stats": stats, "slug": f"m-{slug}-{len(out)}"})
    return out


def fmt(v) -> str:
    if v is None:
        return "no data"
    return f"{v:,.0f}" if abs(v - round(v)) < 1e-9 else f"{v:,.2f}"


def sparkline(vals: list) -> str:
    pts = [v for v in vals if v is not None]
    if not pts:
        return '<svg class="spark" viewBox="0 0 140 30" aria-hidden="true"></svg>'
    lo, hi = min(pts), max(pts)
    span = (hi - lo) or 1
    coords = [f"{i * 10},{28 - 26 * ((v - lo) / span):.1f}" for i, v in enumerate(vals) if v is not None]
    return f'<svg class="spark" viewBox="0 0 140 30" aria-hidden="true"><polyline points="{" ".join(coords)}" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def ring(pct) -> str:
    p = 0 if pct is None else pct
    c = 2 * math.pi * 26
    return (f'<svg class="ring" viewBox="0 0 64 64" role="img" aria-label="{p:.0f}% of target"><circle cx="32" cy="32" r="26" class="ring-bg"/>'
            f'<circle cx="32" cy="32" r="26" class="ring-fg" stroke-dasharray="{c * p / 100:.1f} {c:.1f}" transform="rotate(-90 32 32)"/>'
            f'<text x="32" y="36" text-anchor="middle">{p:.0f}%</text></svg>')


def bars(vals: list) -> str:
    pts = [v for v in vals if v is not None]
    hi = max([abs(v) for v in pts] + [1])
    w = 300 / max(len(vals), 1)
    rects = "".join(f'<rect x="{i * w + 1:.1f}" y="{98 - 90 * abs(v) / hi:.1f}" width="{w - 2:.1f}" height="{90 * abs(v) / hi:.1f}" rx="2"/>'
                    for i, v in enumerate(vals) if v)
    return f'<svg class="bars" viewBox="0 0 300 100" preserveAspectRatio="none" role="img" aria-label="Last 30 days">{rects}</svg>'


def build_html(cfg: dict, cards: list, log: list, todos: list, today: dt.date, theme: str = "glass") -> str:
    e = html.escape
    title = e(str(cfg.get("title") or "My dashboard"))
    card_html, details = [], []
    for c in cards:
        bar = "" if c["pct"] is None else f'<div class="bar" role="progressbar" aria-valuenow="{c["pct"]:.0f}" aria-valuemin="0" aria-valuemax="100"><span style="width:{c["pct"]:.0f}%"></span></div>'
        goal = "" if c.get("target") is None else f' / {fmt(c["target"])}'
        gauge = (ring(c["pct"]) if c["pct"] is not None else "") if theme == "jarvis" else bar
        card_html.append(f'<section class="card glass"><h2>{e(c["name"])}</h2><div class="head"><p class="big">{fmt(c["now"])}<small>{e(goal)} {e(c.get("unit") or "")}</small></p>{gauge if theme == "jarvis" else ""}</div>'
                         f'{"" if theme == "jarvis" else bar}<p class="meta">{e(c.get("period", "all"))} · {c["entries"]} entries</p>{sparkline(c["spark"])}'
                         f'<a class="more" href="#{c["slug"]}">Details <span aria-hidden="true">&rsaquo;</span></a></section>')
        st = c["stats"]
        label_all = "All-time total" if c.get("how", "sum") == "sum" else "Latest"
        tiles = "".join(f'<div class="tile glass"><span>{k}</span><b>{v}</b></div>' for k, v in [
            (f"This {c.get('period', 'all') if c.get('period') != 'all' else 'total'}", fmt(c["now"]) + e(goal)),
            (label_all, fmt(st["all"])), ("Average per day logged", fmt(st["avg"])), ("Best day", fmt(st["best"])),
            ("Days logged", str(st["days"])), ("Current streak", f'{st["streak"]} day{"s" if st["streak"] != 1 else ""}')])
        prog = f'<div class="card glass wide"><h2>Progress to target</h2>{bar}</div>' if bar else ""
        empty_row = "<tr><td>No entries yet.</td></tr>"
        rows_h = "".join(f'<tr><td>{d.isoformat()}</td><td>{fmt(v)}</td><td>{e(n)}</td></tr>' for d, v, n in reversed(c["hist"]))
        details.append(f'<section class="detail" id="{c["slug"]}"><a class="back" href="#top"><span aria-hidden="true">&lsaquo;</span> Overview</a>'
                       f'<h1>{e(c["name"])}</h1><p class="sub">{e(c.get("unit") or "")} · {e(c.get("period", "all"))} · {"adds up" if c.get("how", "sum") == "sum" else "latest value counts"}</p>'
                       f'<div class="tiles">{tiles}</div>{prog}'
                       f'<div class="card glass wide"><h2>Last 30 days</h2>{bars(c["month"])}</div>'
                       f'<div class="card glass wide"><h2>Every entry ({len(c["hist"])})</h2><table>{rows_h or empty_row}</table></div></section>')
    recent = sorted(log, key=lambda r: str(r.get("date", "")), reverse=True)[:6]
    log_rows = "".join(f'<tr><td>{e(str(r.get("date", "")))}</td><td>{e(str(r.get("metric", "")))}</td><td>{e(fmt(number(r.get("value"))) if number(r.get("value")) is not None else str(r.get("value", "")))}</td><td>{e(str(r.get("note", "")))}</td></tr>' for r in recent)
    open_todos = [t for t in todos if str(t.get("status", "open")).strip().lower() != "done"]
    todo_rows = "".join(f'<li><span>{e(str(t.get("item", "")))}</span><time>{e(str(t.get("due", "")))}</time></li>' for t in sorted(open_todos, key=lambda t: str(t.get("due") or "9999")))
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root{{--ink:#1d1d1f;--mute:#6e6e73;--glass:rgba(255,255,255,.55);--edge:rgba(255,255,255,.7);--line:rgba(0,0,0,.08);
--track:rgba(0,0,0,.08);--accent:#0a84ff;--bg1:#f5f5f7;--blob1:#a5c8ff;--blob2:#ffc6e0;--blob3:#c8f2dc}}
@media (prefers-color-scheme:dark){{:root{{--ink:#f5f5f7;--mute:#a1a1a6;--glass:rgba(40,40,46,.55);--edge:rgba(255,255,255,.12);
--line:rgba(255,255,255,.08);--track:rgba(255,255,255,.12);--bg1:#000;--blob1:#1f3a8a;--blob2:#6b1d4f;--blob3:#0f5132}}}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;color:var(--ink);background:var(--bg1);
font:15px/1.45 -apple-system,BlinkMacSystemFont,"SF Pro Text","SF Pro Display","Helvetica Neue",Inter,"Segoe UI",sans-serif;
-webkit-font-smoothing:antialiased;overflow-x:hidden}}
body::before,body::after,main::before{{content:"";position:fixed;z-index:-1;border-radius:50%;filter:blur(90px);opacity:.75}}
body::before{{width:520px;height:520px;background:var(--blob1);top:-140px;left:-120px}}
body::after{{width:460px;height:460px;background:var(--blob2);bottom:-160px;right:-100px}}
main::before{{width:380px;height:380px;background:var(--blob3);top:40%;left:45%}}
main{{max-width:1120px;margin:0 auto;padding:44px 22px 60px}}
h1{{margin:0;font-size:34px;font-weight:700;letter-spacing:-.02em}} .sub{{color:var(--mute);margin:6px 0 26px}}
.glass{{background:var(--glass);border:1px solid var(--edge);border-radius:22px;
backdrop-filter:blur(24px) saturate(180%);-webkit-backdrop-filter:blur(24px) saturate(180%);
box-shadow:0 1px 1px rgba(0,0,0,.04),0 12px 40px rgba(0,0,0,.08)}}
.grid{{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}}
.card{{padding:20px 20px 16px}} .card h2{{margin:0;font-size:13px;font-weight:600;color:var(--mute);letter-spacing:.01em}}
.big{{font-size:40px;font-weight:700;letter-spacing:-.03em;margin:8px 0 12px;font-variant-numeric:tabular-nums}}
.big small{{font-size:15px;font-weight:500;color:var(--mute);letter-spacing:0;margin-left:6px}}
.bar{{height:6px;background:var(--track);border-radius:99px;overflow:hidden}}
.bar span{{display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#5ac8fa,var(--accent))}}
.meta{{color:var(--mute);font-size:12px;margin:10px 0 2px}} .spark{{width:100%;height:34px;color:var(--accent);margin-top:4px}}
.two{{display:grid;gap:16px;grid-template-columns:1fr;margin-top:16px}} @media(min-width:820px){{.two{{grid-template-columns:2fr 1fr}}}}
table{{width:100%;border-collapse:collapse;font-size:14px;margin-top:10px;font-variant-numeric:tabular-nums}}
td{{padding:9px 6px;border-top:1px solid var(--line);vertical-align:top}} td:first-child{{color:var(--mute);white-space:nowrap}}
ul{{list-style:none;margin:10px 0 0;padding:0}} li{{display:flex;justify-content:space-between;gap:12px;padding:10px 0;border-top:1px solid var(--line)}}
li::before{{content:"";flex:none;width:16px;height:16px;border-radius:50%;border:1.5px solid var(--mute);margin-top:2px}}
li span{{flex:1}} time{{color:var(--mute);white-space:nowrap;font-size:13px}}
.more{{display:inline-flex;gap:4px;margin-top:10px;font-size:13px;font-weight:600;color:var(--accent);text-decoration:none;padding:6px 12px;border-radius:99px;background:rgba(10,132,255,.12)}}
.more:hover{{background:rgba(10,132,255,.2)}} .back{{display:inline-flex;gap:6px;color:var(--accent);text-decoration:none;font-weight:600;margin-bottom:14px}}
.detail{{display:none}} .detail:target{{display:block}} main:has(.detail:target) .overview{{display:none}}
.tiles{{display:grid;gap:12px;grid-template-columns:repeat(auto-fill,minmax(160px,1fr))}} .tile{{padding:14px 16px;border-radius:18px}}
.tile span{{display:block;font-size:12px;color:var(--mute)}} .tile b{{display:block;font-size:24px;letter-spacing:-.02em;margin-top:4px;font-variant-numeric:tabular-nums}}
.wide{{margin-top:16px}} .bars{{width:100%;height:120px;margin-top:12px;fill:var(--accent)}}

.jarvis{{--ink:#d9fbff;--mute:#6fb7c4;--glass:rgba(4,22,34,.62);--edge:rgba(0,229,255,.35);--line:rgba(0,229,255,.14);
--track:rgba(0,229,255,.12);--accent:#00e5ff;--bg1:#02080f}}
.jarvis body,body.jarvis{{background:radial-gradient(1200px 700px at 50% -10%,#06324a 0%,#02080f 60%) fixed,
linear-gradient(rgba(0,229,255,.05) 1px,transparent 1px) 0 0/40px 40px,linear-gradient(90deg,rgba(0,229,255,.05) 1px,transparent 1px) 0 0/40px 40px,#02080f;
font-family:"SF Mono",ui-monospace,Menlo,Consolas,monospace;color:var(--ink)}}
body.jarvis::before,body.jarvis::after,body.jarvis main::before{{display:none}}
body.jarvis h1{{text-transform:uppercase;letter-spacing:.18em;font-size:26px;text-shadow:0 0 18px rgba(0,229,255,.55)}}
body.jarvis .sub{{letter-spacing:.08em;text-transform:uppercase;font-size:12px}}
body.jarvis .glass{{border-radius:6px;position:relative;box-shadow:0 0 0 1px rgba(0,229,255,.12) inset,0 0 30px rgba(0,229,255,.08)}}
body.jarvis .glass::before,body.jarvis .glass::after{{content:"";position:absolute;width:14px;height:14px;border:2px solid var(--accent);pointer-events:none}}
body.jarvis .glass::before{{top:-1px;left:-1px;border-right:0;border-bottom:0}} body.jarvis .glass::after{{bottom:-1px;right:-1px;border-left:0;border-top:0}}
body.jarvis .card h2{{text-transform:uppercase;letter-spacing:.16em;font-size:11px;color:var(--accent)}}
body.jarvis .head{{display:flex;align-items:center;justify-content:space-between;gap:8px}}
body.jarvis .big{{text-shadow:0 0 14px rgba(0,229,255,.45);margin:6px 0}} body.jarvis .big small{{display:block;margin:2px 0 0;font-size:13px}}
.ring{{width:74px;height:74px;flex:none}} .ring-bg{{fill:none;stroke:var(--track);stroke-width:5}}
.ring-fg{{fill:none;stroke:var(--accent);stroke-width:5;stroke-linecap:round;filter:drop-shadow(0 0 4px var(--accent))}}
.ring text{{fill:var(--ink);font-size:13px;font-family:inherit}}
body.jarvis .spark{{filter:drop-shadow(0 0 4px var(--accent))}} body.jarvis .bars{{filter:drop-shadow(0 0 6px rgba(0,229,255,.6))}}
body.jarvis .more{{border-radius:4px;background:rgba(0,229,255,.1);border:1px solid var(--edge);text-transform:uppercase;letter-spacing:.12em;font-size:11px}}
body.jarvis li::before{{border-radius:2px;border-color:var(--accent)}} body.jarvis td:first-child{{color:var(--accent)}}
body.jarvis .tile{{border-radius:6px}} body.jarvis .tile span{{text-transform:uppercase;letter-spacing:.12em;font-size:10px;color:var(--accent)}}
</style></head><body class="{theme}"><main>
<div class="overview" id="top"><h1>{title}</h1><p class="sub">Updated {today.isoformat()} · built by Super Claude from your own files</p>
<div class="grid">{"".join(card_html) or '<section class="card glass"><h2>Nothing tracked yet</h2><p class="meta">Tell Super Claude what to track.</p></section>'}</div>
<div class="two"><section class="card glass"><h2>Latest entries</h2><table>{log_rows or '<tr><td>No entries yet.</td></tr>'}</table></section>
<section class="card glass"><h2>To do ({len(open_todos)})</h2><ul>{todo_rows or '<li>All clear.</li>'}</ul></section></div></div>
{"".join(details)}
</main></body></html>
"""


def main(argv: list) -> int:
    ap = argparse.ArgumentParser(description="Personal dashboard from your own files.")
    ap.add_argument("cmd", choices=["init", "log", "todo", "build", "show"])
    ap.add_argument("args", nargs="*")
    ap.add_argument("--dir", default="dashboard")
    ap.add_argument("--title", default="My dashboard")
    ap.add_argument("--track", action="append", default=[])
    ap.add_argument("--note", default="")
    ap.add_argument("--date", default="")
    ap.add_argument("--due", default="")
    ap.add_argument("--done", default="")
    ap.add_argument("--out", default="")
    ap.add_argument("--theme", default="", help="glass (Apple-style, default) or jarvis (HUD)")
    ap.add_argument("--today", default="", help=argparse.SUPPRESS)
    try:
        a = ap.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code or 0)
    d = Path(a.dir)
    today = day(a.today) or dt.date.today()
    try:
        if a.cmd == "init":
            if (d / "config.json").exists():
                fail(f"{d} already has a dashboard. Use another --dir, or edit {d / 'config.json'}.")
            d.mkdir(parents=True, exist_ok=True)
            cfg = {"title": a.title, "theme": a.theme if a.theme in THEMES else "glass", "track": [parse_track(s) for s in a.track]}
            (d / "config.json").write_text(json.dumps(cfg, indent=2), encoding="utf-8")
            print(f"Dashboard created in {d} tracking {len(cfg['track'])} things.")
            return 0
        cfg = load_config(d)
        names = {t.get("name") for t in cfg.get("track", []) if isinstance(t, dict)}
        if a.cmd == "log":
            if len(a.args) < 2:
                fail("Usage: dashboard.py log \"Metric name\" VALUE [--note ...] [--date YYYY-MM-DD]")
            metric, value = a.args[0], number(a.args[1])
            if metric not in names:
                fail(f"{metric!r} is not tracked. Tracked: {', '.join(sorted(n for n in names if n)) or 'nothing yet'}.")
            if value is None:
                fail(f"{a.args[1]!r} is not a number.")
            when = day(a.date) if a.date else today
            if when is None:
                fail(f"--date {a.date!r} must look like 2026-11-21.")
            append(d / "log.csv", ["date", "metric", "value", "note"], [when.isoformat(), metric, int(value) if value == int(value) else value, a.note])
            print(f"Logged {fmt(value)} for {metric} on {when.isoformat()}.")
            return 0
        if a.cmd == "todo":
            p = d / "todo.csv"
            if a.done:
                items = rows(p)
                hit = [t for t in items if a.done.lower() in str(t.get("item", "")).lower() and str(t.get("status", "")).lower() != "done"]
                if not hit:
                    fail(f"No open to-do matches {a.done!r}.")
                hit[0]["status"] = "done"
                with open(p, "w", newline="", encoding="utf-8") as fh:
                    w = csv.DictWriter(fh, fieldnames=["item", "due", "status"], extrasaction="ignore")
                    w.writeheader()
                    w.writerows(items)
                print(f"Done: {hit[0].get('item')}")
                return 0
            if not a.args:
                fail("Usage: dashboard.py todo \"What to do\" [--due YYYY-MM-DD]  or  --done \"words from the item\"")
            if a.due and day(a.due) is None:
                fail(f"--due {a.due!r} must look like 2026-11-27.")
            append(p, ["item", "due", "status"], [" ".join(a.args), a.due, "open"])
            print("Added to-do.")
            return 0
        log, todos = rows(d / "log.csv"), rows(d / "todo.csv")
        cards = summarise(cfg, log, today)
        if a.cmd == "show":
            for c in cards:
                goal = "" if c.get("target") is None else f" of {fmt(c['target'])}"
                print(" ".join(x for x in [f"- {c['name']}: {fmt(c['now'])}{goal}", c.get('unit') or '', f"({c.get('period', 'all')})"] if x))
            open_n = sum(1 for t in todos if str(t.get("status", "open")).lower() != "done")
            print(f"- To do: {open_n} open")
            return 0
        out = Path(a.out) if a.out else d / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        theme = a.theme if a.theme in THEMES else (cfg.get("theme") if cfg.get("theme") in THEMES else "glass")
        out.write_text(build_html(cfg, cards, log, todos, today, theme), encoding="utf-8")
        print(f"Dashboard written to {out}")
        return 0
    except OSError as exc:
        fail(f"Could not read or write the dashboard files: {exc.strerror or exc}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
