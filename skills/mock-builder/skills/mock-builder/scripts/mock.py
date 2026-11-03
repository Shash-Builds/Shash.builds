#!/usr/bin/env python3
"""Mock builder: a one-page website mock for a local service business, as ONE html file.

    python3 mock.py --name "Demo Roofing" --trade "Roofing" --city "Tulsa" --state OK --out previews/demo-roofing/index.html
    python3 mock.py ... --color "#1f6f8b" --logo https://their-site.com/logo.png --phone "(918) 555-0100"

Only the name, trade, city and state are needed. Everything else on the page is clearly marked
as sample: placeholder services, a "your Google reviews go here" panel (never fake reviews),
and a sample banner at the top. --color and --logo should come from the business's own public
website; --phone only if it is the business's public number.

Deploy: put each mock at previews/<slug>/index.html in one static site (Netlify drop, GitHub
Pages) and share https://<your-site>/previews/<slug>/.
"""
import argparse
import html
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = os.path.join(HERE, "..", "templates", "style.css")
SERVICES = {
    "roof": ["Roof repair", "Roof replacement", "Storm damage inspection", "Gutters"],
    "plumb": ["Leak repair", "Water heaters", "Drain cleaning", "Fixture installs"],
    "hvac": ["AC repair", "Heating repair", "New system installs", "Maintenance plans"],
    "clean": ["Standard cleaning", "Deep cleaning", "Move-in and move-out", "Office cleaning"],
    "landscap": ["Lawn care", "Landscape design", "Mulch and planting", "Seasonal cleanup"],
    "paint": ["Interior painting", "Exterior painting", "Cabinets", "Drywall repair"],
    "electric": ["Repairs and troubleshooting", "Panel upgrades", "Lighting", "EV chargers"],
    "pest": ["General pest control", "Termites", "Rodents", "Mosquito treatments"],
    "detail": ["Interior detail", "Exterior detail", "Ceramic coating", "Fleet service"],
}
e = lambda s: html.escape((s or "").strip())


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def text_on(hex_color):
    """Black or white text, whichever reads better on the color (WCAG relative luminance)."""
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    lin = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    lum = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return "#111111" if (lum + 0.05) / 0.05 > 1.05 / (lum + 0.05) else "#ffffff"


def build(name, trade, city, state, color="", logo="", phone="", by=""):
    services = next((v for k, v in SERVICES.items() if k in trade.lower()), ["Service one", "Service two", "Service three", "Service four"])
    css = open(CSS, encoding="utf-8").read()
    if color and re.fullmatch(r"#?[0-9a-fA-F]{3}([0-9a-fA-F]{3})?", color):
        color = "#" + color.lstrip("#")
        css += f"\n.btn-ink{{background:{color};color:{text_on(color)}}}\n.btn-ink:hover{{background:{color};filter:brightness(.92)}}\n"
    tel = "".join(c for c in phone if c.isdigit() or c == "+")
    call = (f'<a class="btn btn-ink" href="tel:{tel}">Call {e(phone)}</a>' if tel
            else '<a class="btn btn-ink" href="#quote">Call (your number)</a>')
    mark = (f'<img src="{e(logo)}" alt="{e(name)} logo" style="height:40px;width:auto">' if logo else e(name))
    rows = "".join(f'<li><b>{e(s)}</b><span class="pill">Sample</span></li>' for s in services)
    made = f" by {e(by)}" if by else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(name)} | {e(trade)} in {e(city)} (sample mock)</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head>
<body>
<div class="ribbon"><div class="wrap"><span>Sample mock{made} for {e(name)}. Services and text are placeholders, not claims about the business.</span></div></div>
<header class="bar"><div class="wrap"><a class="mark" href="#top">{mark}</a>{call}</div></header>
<main id="top">
<section class="hero"><div class="wrap">
<div><h1>{e(trade)} in {e(city)}, done right.</h1>
<p class="lede">Sample headline. Your real promise goes here: what you do, where, and why people pick you.</p>
<div class="actions">{call.replace('btn btn-ink', 'btn btn-ink', 1)}<a class="btn btn-line" href="#quote">Get a free quote</a></div></div>
<div data-slot="hero"><div style="aspect-ratio:4/3;border-radius:var(--radius-card);background:var(--color-paper-3);display:grid;place-items:center;color:var(--color-muted);text-align:center;padding:24px">Your best job photo goes here</div></div>
</div></section>
<section class="block band"><div class="wrap facts">
<dl><dt>Where we work</dt><dd>{e(city)} and nearby (sample)</dd></dl>
<dl><dt>Hours</dt><dd>Your hours here</dd></dl>
<dl><dt>Call or text</dt><dd>{e(phone) or "Your number here"}</dd></dl>
<dl><dt>Based in</dt><dd>{e(city)}, {e(state)}</dd></dl>
</div></section>
<section class="block"><div class="wrap split">
<div><h2>What we do</h2><ul class="rows">{rows}</ul></div>
<div id="quote"><h2>Get a free quote</h2>
<form class="quote" onsubmit="return false">
<label>Your name<input name="name" autocomplete="name"></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel"></label>
<label>What do you need?<textarea name="job" rows="3"></textarea></label>
<button class="btn btn-ink" type="submit" disabled>Send request</button>
<p class="note">Mock only: on the live site, every request lands in your lead sheet with where it came from.</p>
</form></div></div></section>
<section class="block"><div class="wrap"><h2>What customers say</h2>
<p class="note">Your real Google reviews go here. This mock shows none, because we only use reviews your customers actually wrote.</p></div></section>
</main>
<footer class="colophon"><div class="wrap"><div><b>{e(name)}</b><br>{e(trade)} in {e(city)}, {e(state)}.</div><div>Sample mock{made}. Not affiliated with or approved by the business.</div></div></footer>
<div class="callbar">{call}<a class="btn btn-line" href="#quote">Free quote</a></div>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser(description="One-file one-page mock for a local service business.")
    ap.add_argument("--name", required=True)
    ap.add_argument("--trade", required=True)
    ap.add_argument("--city", required=True)
    ap.add_argument("--state", required=True)
    ap.add_argument("--color", default="", help="brand color from their public site, like #1f6f8b")
    ap.add_argument("--logo", default="", help="logo URL from their public site")
    ap.add_argument("--phone", default="", help="their public phone number")
    ap.add_argument("--by", default="", help="your name or studio, shown in the sample banner")
    ap.add_argument("--out", help="default: previews/<slug>/index.html")
    a = ap.parse_args()
    out = a.out or os.path.join("previews", slugify(a.name), "index.html")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(build(a.name, a.trade, a.city, a.state, a.color, a.logo, a.phone, a.by))
    print(f"Wrote {out}. Share it as https://<your-site>/previews/{slugify(a.name)}/")


if __name__ == "__main__":
    main()
