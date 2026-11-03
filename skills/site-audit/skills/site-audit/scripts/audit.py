#!/usr/bin/env python3
"""Site audit: score how weak a small business website is, with facts only.

    python3 audit.py https://example.com            JSON on stdout
    python3 audit.py example.com --md report.md     also write a short markdown report
    python3 audit.py none --name "Joe's Plumbing"   the business has no website
    python3 audit.py URL --no-links                 skip the broken-link check

What it fetches: robots.txt, then the one page you name (GET). If --no-links is not set it
also sends HEAD requests to at most 15 links found on that page. Nothing else. If robots.txt
disallows the page, it stops and says so.

Score: 0 to 100, higher means a weaker site (a better prospect for a rebuild). Every problem
comes with the evidence that proves it. Standard library only.
"""
import argparse
import datetime
import html.parser
import json
import re
import socket
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser

UA = "shashbuilds-site-audit/1.0 (+https://github.com/Shash-Builds/shash.builds/tree/main/skills/site-audit)"
TIMEOUT = 15
MAX_BYTES = 5_000_000
MAX_LINKS = 15
YEAR = datetime.date.today().year

# weight = how much the problem adds to the weak-site score (they sum past 100; the score caps)
WEIGHTS = {
    "no_website": 100, "unreachable": 90, "no_https": 25, "not_mobile": 25, "no_call_button": 20,
    "slow": 15, "heavy": 10, "no_reviews": 12, "outdated": 15, "no_service_area": 10,
    "broken_links": 10, "no_google_business": 8, "no_title": 5,
}
STATES = ("AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ "
          "NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY DC").split()
STATE_NAMES = ("alabama alaska arizona arkansas california colorado connecticut delaware florida georgia "
               "hawaii idaho illinois indiana iowa kansas kentucky louisiana maine maryland massachusetts "
               "michigan minnesota mississippi missouri montana nebraska nevada ohio oklahoma oregon "
               "pennsylvania tennessee texas utah vermont virginia washington wisconsin wyoming").split() + [
               "new hampshire", "new jersey", "new mexico", "new york", "north carolina", "north dakota",
               "rhode island", "south carolina", "south dakota", "west virginia"]
ACTION_WORDS = re.compile(r"\b(call( us| now| today)?|book( now| online| a)?|schedule|get a (free )?(quote|estimate)|"
                          r"request (a )?(quote|estimate|service)|free (quote|estimate)|contact us|appointment)\b", re.I)
GBP = re.compile(r"(google\.[a-z.]+/maps|maps\.google\.|g\.page/|maps\.app\.goo\.gl|goo\.gl/maps|business\.google\.com|search\.google\.com/local)", re.I)
REVIEW = re.compile(r"\b(reviews?|testimonials?|what (our )?(customers|clients) say|stars?|rated)\b", re.I)


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.viewport = None
        self.title = ""
        self._in = []
        self.links = []          # (href, text)
        self.buttons = []        # visible text of buttons and inputs
        self.text = []
        self.scripts = 0
        self.ext_scripts = 0
        self.images = 0
        self.old_tags = set()
        self.generator = ""
        self.ld = []
        self._a = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        self._in.append(tag)
        if tag == "meta":
            if a.get("name", "").lower() == "viewport":
                self.viewport = a.get("content", "")
            if a.get("name", "").lower() == "generator":
                self.generator = a.get("content", "")
        elif tag == "a":
            self._a = [a.get("href", ""), ""]
        elif tag == "script":
            self.scripts += 1
            if a.get("src"):
                self.ext_scripts += 1
            if "ld+json" in a.get("type", ""):
                self.ld.append("")
        elif tag == "img":
            self.images += 1
        elif tag in ("font", "marquee", "center", "frameset", "blink"):
            self.old_tags.add(tag)
        elif tag in ("embed", "object") and "flash" in (a.get("type", "") + a.get("src", "") + a.get("data", "")).lower():
            self.old_tags.add("flash")
        elif tag == "input" and a.get("type", "").lower() in ("submit", "button"):
            self.buttons.append(a.get("value", ""))

    def handle_endtag(self, tag):
        if tag == "a" and self._a is not None:
            self.links.append(tuple(self._a))
            self._a = None
        while self._in and self._in.pop() != tag:
            pass

    def handle_data(self, data):
        top = self._in[-1] if self._in else ""
        if top == "title":
            self.title += data
        if top == "script":
            if self.ld and self._in and "script" in self._in:
                self.ld[-1] += data
            return
        if top == "style":
            return
        if self._a is not None:
            self._a[1] += data
        if top == "button":
            self.buttons.append(data)
        self.text.append(data)


def problem(key, sentence, evidence):
    return {"id": key, "weight": WEIGHTS[key], "problem": sentence, "evidence": evidence}


def fetch(url, method="GET"):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    start = time.monotonic()
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ssl.create_default_context()) as r:
        first = time.monotonic() - start
        body = r.read(MAX_BYTES) if method == "GET" else b""
        return r.geturl(), r.status, r.headers, body, first, time.monotonic() - start


def robots_allows(url):
    parts = urllib.parse.urlsplit(url)
    rp = urllib.robotparser.RobotFileParser()
    robots = f"{parts.scheme}://{parts.netloc}/robots.txt"
    try:
        req = urllib.request.Request(robots, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ssl.create_default_context()) as r:
            rp.parse(r.read(200_000).decode("utf-8", "replace").splitlines())
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False, robots          # standard: treat as disallow all
        return True, robots               # 404 etc: no rules
    except Exception:
        return True, robots
    return rp.can_fetch(UA, url), robots


def check_links(base, links):
    host = urllib.parse.urlsplit(base).netloc
    seen, out = [], []
    for href, _ in links:
        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:", "sms:")):
            continue
        u = urllib.parse.urljoin(base, href).split("#")[0]
        if u in seen or not u.startswith("http") or u.rstrip("/") == base.rstrip("/"):
            continue
        seen.append(u)
    seen.sort(key=lambda u: urllib.parse.urlsplit(u).netloc != host)  # own pages first
    for u in seen[:MAX_LINKS]:
        try:
            try:
                fetch(u, "HEAD")
            except urllib.error.HTTPError as e:
                if e.code in (403, 405, 429, 501):   # many servers refuse HEAD or bots; not proof of a broken link
                    continue
                out.append({"url": u, "status": e.code})
        except (urllib.error.URLError, socket.timeout, ssl.SSLError, ConnectionError) as e:
            reason = str(getattr(e, "reason", e))
            if "Name or service not known" in reason or "nodename nor servname" in reason or "getaddrinfo" in reason:
                out.append({"url": u, "status": "domain does not resolve"})
    return out, min(len(seen), MAX_LINKS)


def audit(target, name="", check_broken=True):
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    result = {"input": target, "business": name, "checked_at": now, "tool": "shash.builds site-audit 1.0",
              "fetched": [], "facts": {}, "problems": []}
    if target.strip().lower() in ("", "none", "no website", "no-website", "-"):
        result["problems"].append(problem("no_website", "The business has no website, so people who search for it find only directory listings.",
                                          "No website was given or found."))
        return finish(result)
    url = target.strip()
    if not re.match(r"https?://", url, re.I):
        url = "https://" + url
    allowed, robots = robots_allows(url)
    result["fetched"].append(robots)
    if not allowed:
        result["skipped"] = "robots.txt asks automated tools not to fetch this page, so it was not audited."
        return finish(result)
    try:
        final, status, headers, body, ttfb, total = fetch(url)
    except ssl.SSLError as e:
        result["fetched"].append(url)
        result["problems"].append(problem("no_https", "The secure (https) version of the site shows a security error, so browsers warn visitors away.",
                                          f"TLS error on {url}: {e.__class__.__name__}"))
        return finish(result)
    except urllib.error.HTTPError as e:
        result["fetched"].append(url)
        result["problems"].append(problem("unreachable", f"The homepage returns an error ({e.code}) instead of the site.", f"HTTP {e.code} on {url}"))
        return finish(result)
    except Exception as e:
        result["fetched"].append(url)
        if url.startswith("https://"):
            try:   # some small sites only answer on http; one retry, still the same page
                final, status, headers, body, ttfb, total = fetch("http://" + url[8:])
                result["fetched"].append("http://" + url[8:])
            except Exception:
                result["problems"].append(problem("unreachable", "The website does not load at all.", f"{url}: {e.__class__.__name__}"))
                return finish(result)
        else:
            result["problems"].append(problem("unreachable", "The website does not load at all.", f"{url}: {e.__class__.__name__}"))
            return finish(result)
    result["fetched"].append(url)
    charset = headers.get_content_charset() or "utf-8"
    doc = body.decode(charset, "replace")
    p = Page()
    try:
        p.feed(doc)
    except Exception:
        pass
    text = " ".join(" ".join(p.text).split())
    low = text.lower()
    f = result["facts"]
    f.update({"final_url": final, "status": status, "https": final.startswith("https://"),
              "seconds_to_first_byte": round(ttfb, 2), "seconds_to_download": round(total, 2),
              "html_kb": round(len(body) / 1024), "scripts": p.scripts, "script_files": p.ext_scripts, "images": p.images,
              "title": " ".join(p.title.split())[:120], "viewport": p.viewport, "generator": p.generator})

    if not f["https"]:
        result["problems"].append(problem("no_https", "The site is not secure (no https), so Chrome labels it \"Not secure\" next to the address.",
                                          f"Page loaded from {final}"))
    vp = (p.viewport or "").lower()
    if "width=device-width" not in vp:
        result["problems"].append(problem("not_mobile", "The site is not set up for phones, so on a phone it shows as a tiny desktop page.",
                                          "No <meta name=\"viewport\" content=\"width=device-width...\"> tag" + (f" (found: {p.viewport!r})" if p.viewport else "")))
    tel = [h for h, _ in p.links if h.lower().startswith("tel:")]
    actions = [t.strip() for _, t in p.links if ACTION_WORDS.search(t or "")] + [b.strip() for b in p.buttons if ACTION_WORDS.search(b or "")]
    f["tel_links"] = len(tel)
    f["action_buttons"] = actions[:5]
    if not tel and not actions:
        result["problems"].append(problem("no_call_button", "There is no tap-to-call or booking button, so a visitor on a phone has to copy the number by hand.",
                                          "No tel: link and no link or button that says call, book, schedule, quote or estimate"))
    elif not tel:
        f["note_no_tel"] = "Has an action button but no tel: link"
    if total > 4:
        result["problems"].append(problem("slow", f"The homepage took {total:.1f} seconds to download from our test server; most visitors leave a slow page.",
                                          f"{total:.2f} s total, {ttfb:.2f} s to first byte, one GET from the audit server"))
    if len(body) > 1_500_000 or p.ext_scripts > 60:
        result["problems"].append(problem("heavy", f"The homepage makes a phone download {p.ext_scripts} separate script files and {round(len(body)/1024)} KB of HTML before it is usable, which is slow on a cell connection.",
                                          f"{round(len(body)/1024)} KB of HTML, {p.ext_scripts} external script files"))
    ld = " ".join(p.ld).lower()
    has_rating = "aggregaterating" in ld or "reviewrating" in ld
    if not REVIEW.search(low) and not has_rating:
        result["problems"].append(problem("no_reviews", "The homepage shows no customer reviews, so a new visitor has no proof the business is good.",
                                          "No review, testimonial or rating text and no rating markup on the page"))
    years = [int(y) for y in re.findall(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?((?:19|20)\d{2})", doc, re.I)]
    old = sorted(p.old_tags)
    if years and max(years) <= YEAR - 3:
        old.append(f"copyright {max(years)}")
    gen = p.generator.lower()
    m = re.search(r"wordpress (\d+)\.", gen)
    if m and int(m.group(1)) < 5:
        old.append(p.generator)
    if re.search(r"jquery[.-]?1\.\d+(\.\d+)?(\.min)?\.js", doc, re.I):
        old.append("jQuery 1.x")
    if old:
        result["problems"].append(problem("outdated", "The site shows signs of not being updated in years, which makes the business look closed or behind.",
                                          "Found: " + ", ".join(old)))
    states_found = [s for s in STATES if re.search(rf"\b{s}\b(?:\s+\d{{5}})?", text)] + [s for s in STATE_NAMES if s in low]
    area = re.search(r"\b(serving|service areas?|areas? (we )?serve|proudly serv|locally owned|near you|in and around)\b", low)
    if not states_found and not area and "areaserved" not in ld:
        result["problems"].append(problem("no_service_area", "The homepage never says which towns the business serves, so locals can't tell if it covers them.",
                                          "No US state, service-area phrase or areaServed markup on the page"))
    if not any(GBP.search(h) for h, _ in p.links) and not GBP.search(doc):
        result["problems"].append(problem("no_google_business", "The site does not link to the business's Google profile, where its reviews and map live.",
                                          "No link to Google Maps or a Google Business Profile"))
    if not f["title"]:
        result["problems"].append(problem("no_title", "The page has no title, so Google shows a blank or messy headline for it.", "Empty <title>"))
    if check_broken:
        broken, checked = check_links(final, p.links)
        f["links_checked"] = checked
        if broken:
            result["problems"].append(problem("broken_links", f"{len(broken)} link(s) on the homepage are broken, so visitors hit error pages.",
                                              "; ".join(f"{b['url']} ({b['status']})" for b in broken[:3])))
    return finish(result)


def finish(result):
    probs = sorted(result["problems"], key=lambda x: -x["weight"])
    result["problems"] = probs
    result["score"] = min(100, sum(x["weight"] for x in probs))
    result["top_3"] = [x["problem"] for x in probs[:3]]
    return result


def markdown(r):
    who = r["business"] or r["input"]
    lines = [f"# Site audit: {who}", "", f"Checked {r['checked_at']} by shash.builds site-audit.", ""]
    if r.get("skipped"):
        return "\n".join(lines + [r["skipped"], ""])
    lines += [f"**Weak-site score: {r['score']}/100** (higher means more room to improve)", "", "## Top problems", ""]
    for i, x in enumerate(r["problems"][:3], 1):
        lines.append(f"{i}. {x['problem']}  \n   Evidence: {x['evidence']}")
    if not r["problems"]:
        lines.append("No problems found by these checks.")
    if len(r["problems"]) > 3:
        lines += ["", "## Also found", ""] + [f"- {x['problem']}" for x in r["problems"][3:]]
    lines += ["", "Fetched: " + ", ".join(r["fetched"]) if r["fetched"] else ""]
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="Weak-site score and provable problems for one website.")
    ap.add_argument("url", help='the website, or "none" if the business has no site')
    ap.add_argument("--name", default="", help="business name, for the report")
    ap.add_argument("--md", help="also write a markdown report to this file")
    ap.add_argument("--no-links", action="store_true", help="skip the broken-link HEAD checks")
    a = ap.parse_args()
    r = audit(a.url, a.name, not a.no_links)
    if a.md:
        with open(a.md, "w", encoding="utf-8") as fh:
            fh.write(markdown(r))
    json.dump(r, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
