#!/usr/bin/env python3
"""Build the shash.builds concept sites: one self-contained index.html per sample.

    python3 portfolio/build.py            # build every portfolio/<slug>/site.json
    python3 portfolio/build.py roofer-tx  # build one

Each sample folder holds:
    site.json   all copy, colors, photos and the lookbook style to use
    img/        WebP photos (made from the source photos by this script, see "photos")
    index.html  built output, never edit by hand

The look comes from the lookbook's 8 styles (styles/s1.css to s8.css, one per style) on top of
styles/base.css, which keeps the Mock Builder skill's rules: a call button in the first screen,
a sticky call bar on phones, a demo form that sends nothing, and a reviews panel that stays empty
because we never make reviews up.
"""
import html
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STYLES = os.path.join(HERE, "styles")
GALLERY = "../"  # the gallery page, relative to each sample
e = lambda s: html.escape(str(s or ""), quote=True)


def tel(phone):
    return "+1" + "".join(c for c in phone if c.isdigit())


def css_for(style):
    parts = [open(os.path.join(STYLES, f), encoding="utf-8").read() for f in ("base.css", f"{style}.css")]
    css = "\n".join(parts)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)  # comments stay in the source files
    css = re.sub(r"\s*\n\s*", "\n", css).strip()
    return css


def photos(slug, site):
    """Make img/<name>.webp (and a 640w copy) from each photo's source file, if missing."""
    out = os.path.join(HERE, slug, "img")
    os.makedirs(out, exist_ok=True)
    for p in site["photos"].values():
        src = p.get("src")
        big = os.path.join(out, p["file"] + ".webp")
        if src and not os.path.exists(big):
            for w, path in ((1280, big), (640, os.path.join(out, p["file"] + "-640.webp"))):
                subprocess.run(["convert", src, "-resize", f"{w}x>", "-strip", "-quality", "72", path], check=True)


def img(site, key, cls="", eager=False, sizes="(min-width: 60rem) 50vw, 100vw"):
    p = site["photos"][key]
    f = "img/" + p["file"]
    w, h = p["w"], p["h"]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{f}.webp" srcset="{f}-640.webp 640w, {f}.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(p["alt"])}" {load}>')


def build(slug):
    site = json.load(open(os.path.join(HERE, slug, "site.json"), encoding="utf-8"))
    photos(slug, site)
    b = site["business"]
    phone, call_label = b["phone"], site.get("call_label", "Call " + b["phone"])
    call = f'<a class="btn btn-call" href="tel:{tel(phone)}">{e(call_label)}</a>'
    book = f'<a class="btn btn-book" href="#quote">{e(site["book_label"])}</a>'
    primary, secondary = (book, call) if site.get("book_first") else (call, book)
    fonts = site["fonts"]

    nav = "".join(f'<a href="#{k}">{e(v)}</a>' for k, v in (("services", "Services"), ("area", "Service area"), ("about", "About"), ("faq", "FAQ")))
    facts = "".join(f"<li>{e(f)}</li>" for f in site["hero"]["facts"])
    services = "".join(
        f'<li><span class="n" aria-hidden="true">{i + 1:02d}</span><h3>{e(s[0])}</h3><p>{e(s[1])}</p></li>'
        for i, s in enumerate(site.get("services", [])))
    steps = "".join(f"<li><h3>{e(s[0])}</h3><p>{e(s[1])}</p></li>" for s in site["steps"])
    towns = "".join(f"<li>{e(t)}</li>" for t in site["area"]["towns"])
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in site["faq"])
    hours = "".join(f"<dt>{e(d)}</dt><dd>{e(t)}</dd>" for d, t in site["hours"])
    options = "".join(f"<option>{e(o)}</option>" for o in site["form"]["options"])
    credits = "; ".join(f'<a href="{e(p["credit_url"])}">{e(p["credit"])}</a>' for p in site["photos"].values())

    estimator = ""
    if site.get("estimator"):
        est = site["estimator"]
        sel = lambda name, label, opts: (f'<label>{e(label)}<select name="{name}">' +
                                         "".join(f'<option value="{v}"{" selected" if i == 1 else ""}>{e(t)}</option>' for i, (t, v) in enumerate(opts)) + "</select></label>")
        estimator = f"""<section class="estimator block" aria-labelledby="est-h"><div class="wrap est-card">
<div><p class="eyebrow">Price check</p><h2 id="est-h">{e(est["title"])}</h2><p>{e(est["note"])}</p></div>
<form class="est" id="est">{sel("beds", "Bedrooms", est["beds"])}{sel("baths", "Bathrooms", est["baths"])}{sel("freq", "How often", est["freq"])}
<output id="est-out" for="est" aria-live="polite"><span>Estimated price per visit</span><b>$0</b></output></form>
</div></section>"""

    est_js = ""
    if site.get("estimator"):
        est_js = """const est=document.getElementById('est');if(est){const run=()=>{const f=new FormData(est);const p=Math.round((+f.get('beds')+ +f.get('baths'))*(+f.get('freq')));est.querySelector('b').textContent='$'+p;};est.addEventListener('change',run);run();}"""

    layout = site.get("hero_layout", "split")
    hero_visual = (f'<figure class="hero-photo hero-art" aria-hidden="true">{site["hero_svg"]}</figure>' if layout == "visual"
                   else f'<figure class="hero-photo">{img(site, "hero", eager=True)}</figure>')
    gkeys = site.get("gallery", [k for k in ("g1", "g2") if k in site["photos"]])
    gallery = ""
    if gkeys:
        figs = "".join(f'<figure>{img(site, k, sizes="(min-width: 60rem) 50vw, 100vw")}</figure>' for k in gkeys)
        gallery = f'<section class="gallery g{len(gkeys)}" aria-label="Photos"><div class="wrap gal">{figs}</div></section>'
    extra = ""
    if site.get("extra"):
        x = site["extra"]
        items = "".join(f'<li><b>{e(i[0])}</b><h3>{e(i[1])}</h3><p>{e(i[2])}</p></li>' for i in x["items"])
        extra = (f'<section class="extra block" aria-labelledby="x-h"><div class="wrap">'
                 f'<div class="head"><p class="eyebrow">{e(x["eyebrow"])}</p><h2 id="x-h">{e(x["title"])}</h2></div>'
                 f'<ul class="xl">{items}</ul></div></section>')
    picker = ""
    if site.get("picker"):
        pk = site["picker"]
        btns = "".join(f'<li><button type="button" class="pick" data-need="{e(t)}">{e(t)}</button></li>' for t in pk["items"])
        picker = (f'<section class="picker block" aria-labelledby="pk-h"><div class="wrap pk-in">'
                  f'<div class="head"><p class="eyebrow">{e(pk["eyebrow"])}</p><h2 id="pk-h">{e(pk["title"])}</h2><p>{e(pk["note"])}</p></div>'
                  f'<ul class="picks">{btns}</ul></div></section>')
    menu = ""
    if site.get("menu"):
        mn = site["menu"]
        rows = "".join(f'<li><div><h3>{e(r[0])}</h3><p>{e(r[1])}</p></div><span class="dots" aria-hidden="true"></span><b>{e(r[2])}</b></li>' for r in mn["items"])
        menu = (f'<section class="menu block" id="{e(mn.get("id", "services"))}" aria-labelledby="menu-h"><div class="wrap menu-in">'
                f'<div class="head"><p class="eyebrow">{e(mn["eyebrow"])}</p><h2 id="menu-h">{e(mn["title"])}</h2><p>{e(mn["note"])}</p></div>'
                f'<ul class="menu-list">{rows}</ul></div></section>')
    preload = ""
    if layout != "visual":
        h = site["photos"]["hero"]
        preload = (f'<link rel="preload" as="image" href="img/{e(h["file"])}-640.webp" imagesrcset="img/{e(h["file"])}-640.webp 640w, '
                   f'img/{e(h["file"])}.webp {h["w"]}w" imagesizes="(min-width: 60rem) 50vw, 100vw">')

    sections = {
        "hero": f"""<section class="hero hero--{layout}"><div class="wrap hero-in">
<div class="hero-copy">
<p class="eyebrow">{e(site["hero"]["eyebrow"])}</p>
<h1>{e(site["hero"]["title"])}</h1>
<p class="lede">{e(site["hero"]["sub"])}</p>
<div class="actions">{primary}{secondary}</div>
<ul class="facts" aria-label="Quick facts">{facts}</ul>
</div>
{hero_visual}
</div></section>""",
        "services": f"""<section class="services block" id="services" aria-labelledby="svc-h"><div class="wrap">
<div class="head"><p class="eyebrow">Services</p><h2 id="svc-h">{e(site.get("services_title", ""))}</h2></div>
<ul class="svc">{services}</ul>
</div></section>""",
        "how": f"""<section class="how block" aria-labelledby="how-h"><div class="wrap how-in">
<div class="head"><p class="eyebrow">How it works</p><h2 id="how-h">{e(site["steps_title"])}</h2></div>
<ol class="steps">{steps}</ol>
</div></section>""",
        "gallery": f"""{gallery}""",
        "area": f"""<section class="area block" id="area" aria-labelledby="area-h"><div class="wrap area-in">
<div class="head"><p class="eyebrow">Service area</p><h2 id="area-h">{e(site["area"]["title"])}</h2><p>{e(site["area"]["note"])}</p></div>
<ul class="towns">{towns}</ul>
</div></section>""",
        "about": f"""<section class="about block" id="about" aria-labelledby="about-h"><div class="wrap about-in">
<div class="head"><p class="eyebrow">About</p><h2 id="about-h">{e(site["about"]["title"])}</h2></div>
<div class="about-body">{"".join(f"<p>{e(p)}</p>" for p in site["about"]["body"])}</div>
</div></section>""",
        "promise": f"""<section class="promise block" aria-labelledby="promise-h"><div class="wrap promise-in">
<div class="guarantee"><p class="eyebrow">Our promise</p><h2 id="promise-h">{e(site["promise"]["title"])}</h2><p>{e(site["promise"]["body"])}</p></div>
<div class="reviews-slot" role="note"><p class="eyebrow">Reviews</p><p class="rs-title">Reviews go here.</p><p>On a live site, this panel shows the business's own Google reviews. A concept site has no customers yet, so it shows none. We never make reviews up.</p></div>
</div></section>""",
        "faq": f"""<section class="faq block" id="faq" aria-labelledby="faq-h"><div class="wrap faq-in">
<div class="head"><p class="eyebrow">FAQ</p><h2 id="faq-h">Questions people ask first</h2></div>
<div class="qs">{faq}</div>
</div></section>""",
        "contact": f"""<section class="contact block" id="quote" aria-labelledby="quote-h"><div class="wrap contact-in">
<div class="head"><p class="eyebrow">{e(site["form"]["eyebrow"])}</p><h2 id="quote-h">{e(site["form"]["title"])}</h2><p>{e(site["form"]["note"])}</p>
<p class="big-call"><a href="tel:{tel(phone)}">{e(phone)}</a></p>
<dl class="hours">{hours}</dl></div>
<form class="quote" id="quote-form" novalidate>
<label>Your name<input name="name" autocomplete="name" required></label>
<label>Phone<input name="phone" type="tel" autocomplete="tel" inputmode="tel" required></label>
<label>{e(site["form"]["where"])}<input name="where" autocomplete="{e(site["form"].get("where_ac", "postal-code"))}"></label>
<label>What do you need?<select name="need">{options}</select></label>
<label>Anything else?<textarea name="msg" rows="3"></textarea></label>
<button class="btn btn-call" type="submit">{e(site["form"]["button"])}</button>
<p class="form-note" id="form-note" role="status">Demo form: it isn't connected, so nothing you type is sent.</p>
</form>
</div></section>""",
        "estimator": estimator,
        "extra": extra,
        "picker": picker,
        "menu": menu,
    }
    if not site.get("services"):
        sections["services"] = ""
    order = site.get("order", ["hero", "services", "estimator", "how", "gallery", "area", "about", "promise", "faq", "contact"])
    body = "\n\n".join(sections[k] for k in order if sections.get(k))

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(b["name"])}: {e(b["trade_title"])} in {e(b["city"])}, {e(b["state"])} (concept site)</title>
<meta name="description" content="{e(site["meta"])}">
<meta name="theme-color" content="{e(site["theme_color"])}">
<meta property="og:title" content="{e(b["name"])}, a concept site by shash.builds">
<meta property="og:description" content="{e(site["meta"])}">
<meta property="og:type" content="website">
<meta property="og:image" content="shots/desktop-1280x720.jpg">
<link rel="icon" href="data:image/svg+xml,{e(site["favicon"])}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
{preload}
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}&display=swap"></noscript>
<style>
{css_for(site["style"])}
</style>
</head>
<body class="{e(site["style"])} {e(slug)}">
<a class="skip" href="#main">Skip to content</a>
<p class="concept-strip">Concept site for a made-up business. <a href="{GALLERY}">See all samples by shash.builds</a></p>
<header class="nav"><div class="wrap nav-in">
<a class="logo" href="#main">{site.get("logo_svg", "")}<span>{e(b["name"])}</span></a>
<nav aria-label="Sections">{nav}</nav>
<a class="btn btn-call nav-cta" href="tel:{tel(phone)}"><span class="narrow">Call</span><span class="wide">Call {e(phone)}</span></a>
</div></header>
<main id="main">
{body}
</main>

<footer class="foot"><div class="wrap foot-in">
<div><p class="logo">{e(b["name"])}</p><p>{e(b["trade_title"])} in {e(b["city"])}, {e(b["state"])}.</p><p><a href="tel:{tel(phone)}">{e(phone)}</a></p></div>
<div class="small"><p>A made-up business. Name, phone (a 555 number) and copy are sample content.{" " + e(site["art_note"]) if site.get("art_note") else ""}</p>{f"<p>Photos: {credits} (CC0 or public domain).</p>" if credits else ""}</div>
<a class="badge" href="{GALLERY}">Concept site by <b>shash.builds</b></a>
</div></footer>
<div class="callbar">{call.replace(e(call_label), "Call now")}<a class="btn btn-book" href="#quote">{e(site["form"]["short"])}</a></div>
<script>
document.getElementById('quote-form').addEventListener('submit',ev=>{{ev.preventDefault();document.getElementById('form-note').textContent='Thanks! This is a demo, so nothing was sent. On a live site, this lands in the owner\\'s inbox and lead sheet.';}});
{est_js}
document.querySelectorAll('[data-need]').forEach(b=>b.addEventListener('click',()=>{{const s=document.querySelector('select[name=need]');[...s.options].forEach(o=>{{if(o.text===b.dataset.need)s.value=o.value;}});document.getElementById('quote').scrollIntoView({{behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'}});setTimeout(()=>s.focus({{preventScroll:true}}),400);}}));
</script>
</body>
</html>
"""
    open(os.path.join(HERE, slug, "index.html"), "w", encoding="utf-8").write(page)
    print("built", slug)


if __name__ == "__main__":
    slugs = sys.argv[1:] or sorted(d for d in os.listdir(HERE) if os.path.isfile(os.path.join(HERE, d, "site.json")))
    for s in slugs:
        build(s)
