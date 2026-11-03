"""One-page starter: builds a one-page website per local service business from a CSV.

Usage:
  python3 build.py businesses.csv [out_dir] [--by "Your studio" --by-url https://...] [--sheet-url URL]

  --by, --by-url   add a "free preview made for <business> by <you>" ribbon and footer
                   credit (for designers sending previews to prospects). Leave out for a live site.
  --sheet-url      the lead tracker's Apps Script web app URL (see ../lead-tracker). Turns the
                   quote form on: every request lands in the Google Sheet with its source.
                   Without it the form is a disabled preview.

Each row becomes out_dir/<slug>/index.html plus the shared CSS. Columns:
slug,name,trade,city,state,phone,rating,reviews_count,services,hours,area,
review1,review1_by,review2,review2_by,review3,review3_by,photo_url,photo_credit,sample
services: separated by |. sample: "yes" labels the page as sample data.
Use only real public facts about the business (name, phone, its own Google reviews).
"""
import argparse, csv, html, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
CAPTURE = os.path.join(HERE, "..", "lead-tracker", "capture.js")
DEFAULT_PHOTO = ("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/"
                 "342_East_Church_Street_Frederick_MD1.jpg/1280px-342_East_Church_Street_Frederick_MD1.jpg")
DEFAULT_CREDIT = ('Stand-in photo: 342 East Church Street, Frederick MD, Wikimedia Commons '
                  '(<a href="https://commons.wikimedia.org/wiki/File:342_East_Church_Street_Frederick_MD1.jpg">source and licence</a>)')

e = lambda s: html.escape((s or "").strip())


def page(r, by="", by_url="", live_form=False):
    name, trade, city = e(r["name"]), e(r["trade"]), e(r["city"])
    phone = e(r["phone"])
    tel = "".join(c for c in r["phone"] if c.isdigit() or c == "+")
    services = [s.strip() for s in (r.get("services") or "").split("|") if s.strip()]
    rows = "\n".join(f'<li><b>{e(s)}</b><span class="pill">Booking now</span></li>' for s in services)
    reviews = ""
    for i in (1, 2, 3):
        t, who = r.get(f"review{i}"), r.get(f"review{i}_by")
        if t and t.strip():
            reviews += f'<figure><blockquote>{e(t)}</blockquote><figcaption>{e(who)}, Google review</figcaption></figure>\n'
    sample = (r.get("sample") or "").lower() == "yes"
    sample_note = '<p class="note">Sample data: this business and its reviews are made up to show the layout.</p>' if sample else ""
    photo = e(r.get("photo_url")) or DEFAULT_PHOTO
    credit = r.get("photo_credit") or DEFAULT_CREDIT
    rating_block = ""
    if r.get("rating"):
        rating_block = (f'<div class="rating"><strong>{e(r["rating"])}</strong>'
                        f'<span>out of 5 from {e(r.get("reviews_count"))} reviews on Google</span></div>')
    ribbon = credit_by = ""
    if by:
        link = f'<a href="{e(by_url)}">Make it yours</a>' if by_url else ""
        ribbon = f'<div class="ribbon"><div class="wrap"><span>A free preview made for {name} by {e(by)}.</span>{link}</div></div>\n'
        credit_by = f"<br>Preview by {e(by)}."
    if live_form:
        form_open = '<form class="quote" id="quote-form">'
        form_end = '<button class="btn btn-ink" type="submit">Send request</button>\n<p class="note">We reply the same day.</p>'
        script, req = '<script src="capture.js" defer></script>', " required"
    else:
        form_open = '<form class="quote" onsubmit="return false">'
        form_end = ('<button class="btn btn-ink" type="submit" disabled>Send request</button>\n'
                    '<p class="note">Preview only: once live, every request lands in your lead sheet with where it came from.</p>')
        script = req = ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} | {trade} in {city}</title>
<meta name="description" content="{name}: {trade.lower()} in {city}, {e(r['state'])}. Call {phone} for a free quote.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Epilogue:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="page.css">{script}</head>
<body>
{ribbon}<header class="bar"><div class="wrap"><a class="mark" href="#top">{name}</a><a class="btn btn-ink" href="tel:{tel}">Call<span class="wide">&nbsp;{phone}</span></a></div></header>
<main id="top">
<section class="hero"><div class="wrap">
<div><h1>{trade} in {city}, done right.</h1>
<p class="lede">Local, on time and fairly priced. Free quotes, same day.</p>
<div class="actions"><a class="btn btn-ink" href="tel:{tel}">Call now</a><a class="btn btn-line" href="#quote">Get a free quote</a></div>
{rating_block}</div>
<div data-slot="hero" data-alt="Work by {name}"><img src="{photo}" alt="Work by {name}" width="1280" height="960"></div>
</div></section>
<section class="block band"><div class="wrap facts">
<dl><dt>Where we work</dt><dd>{e(r.get('area')) or city}</dd></dl>
<dl><dt>Hours</dt><dd>{e(r.get('hours'))}</dd></dl>
<dl><dt>Call or text</dt><dd><a href="tel:{tel}">{phone}</a></dd></dl>
<dl><dt>Based in</dt><dd>{city}, {e(r['state'])}</dd></dl>
</div></section>
<section class="block"><div class="wrap split">
<div><h2>What we do</h2><ul class="rows">{rows}</ul></div>
<div id="quote"><h2>Get a free quote</h2>
{form_open}
<label>Your name<input name="name" autocomplete="name"></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel"{req}></label>
<label>What do you need?<textarea name="job" rows="3"></textarea></label>
{form_end}
</form></div>
</div></section>
<section class="block"><div class="wrap"><h2>What customers say</h2>
<div class="reviews">{reviews}</div>{sample_note}</div></section>
</main>
<footer class="colophon"><div class="wrap">
<div><b>{name}</b><br>{trade} in {city}, {e(r['state'])}. <a href="tel:{tel}">{phone}</a></div>
<div>{credit}{credit_by}</div>
</div></footer>
<div class="callbar"><a class="btn btn-ink" href="tel:{tel}">Call now</a><a class="btn btn-line" href="#quote">Free quote</a></div>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser(description="Build one-page sites for local service businesses from a CSV.")
    ap.add_argument("csv")
    ap.add_argument("out", nargs="?", default=os.path.join(HERE, "out"))
    ap.add_argument("--by", default="", help="your name or studio, for a preview ribbon")
    ap.add_argument("--by-url", default="", help="link for the ribbon's 'Make it yours'")
    ap.add_argument("--sheet-url", default="", help="lead tracker web app URL; turns the form on")
    a = ap.parse_args()
    with open(a.csv, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = os.path.join(a.out, r["slug"])
            os.makedirs(d, exist_ok=True)
            for css in ("tokens.css", "base.css", "page.css"):
                shutil.copy(os.path.join(HERE, css), d)
            if a.sheet_url:
                js = open(CAPTURE, encoding="utf-8").read().replace("PASTE_WEB_APP_URL_HERE", a.sheet_url)
                open(os.path.join(d, "capture.js"), "w", encoding="utf-8").write(js)
            with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as g:
                g.write(page(r, a.by, a.by_url, bool(a.sheet_url)))
            print("built", os.path.join(d, "index.html"))


if __name__ == "__main__":
    main()
