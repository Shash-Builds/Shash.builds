#!/usr/bin/env python3
"""Build the shash.builds media kit: banners, Tab, icons, social preview.

Every word in every SVG is converted to outlines, so the files look the same on
GitHub, in an <img> tag and offline, with no font loading.

    pip install fonttools uharfbuzz
    python3 media/build.py                 # rebuild the whole kit
    python3 media/build.py header "Lead Tracker" --kind tool --out tools/lead-tracker/header.svg

Fonts (SIL Open Font License 1.1, downloaded on first run into media/.fonts/, not committed):
Bricolage Grotesque by Mathieu Triay, Onest by Dmitri Voloshin and Andrey Kudryavtsev.
"""
import argparse
import io
import pathlib
import urllib.request

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / ".fonts"
FONT_URLS = {
    "bricolage": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf",
    "onest": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/onest/Onest%5Bwght%5D.ttf",
}

ORANGE, INK, CREAM = "#e8572c", "#15120f", "#f6efe3"
MUTED = "#b9ad9c"  # cream at roughly 70% on ink, for secondary lines


# ---------- text to outlines ----------

class Face:
    def __init__(self, name, axes):
        CACHE.mkdir(exist_ok=True)
        src = CACHE / f"{name}.ttf"
        if not src.exists():
            urllib.request.urlretrieve(FONT_URLS[name], src)
        font = instantiateVariableFont(TTFont(src), axes)
        buf = io.BytesIO()
        font.save(buf)
        self.blob = buf.getvalue()
        self.font = TTFont(io.BytesIO(self.blob))
        self.glyphs = self.font.getGlyphSet()
        self.order = self.font.getGlyphOrder()
        self.upm = self.font["head"].unitsPerEm

    def shape(self, text):
        face = hb.Face(self.blob)
        font = hb.Font(face)
        buf = hb.Buffer()
        buf.add_str(text)
        buf.guess_segment_properties()
        hb.shape(font, buf, {"kern": True, "liga": True})
        return list(zip(buf.glyph_infos, buf.glyph_positions))

    def width(self, text, size, tracking=0.0):
        s = size / self.upm
        run = self.shape(text)
        return sum(p.x_advance for _, p in run) * s + tracking * size * max(len(run) - 1, 0)

    def path(self, text, size, x, y, tracking=0.0, anchor="start"):
        """SVG path data for `text` with its baseline at y."""
        s = size / self.upm
        if anchor == "middle":
            x -= self.width(text, size, tracking) / 2
        elif anchor == "end":
            x -= self.width(text, size, tracking)
        pen = SVGPathPen(self.glyphs, ntos=lambda v: ('%.1f' % v).rstrip('0').rstrip('.'))
        cx = x
        for info, pos in self.shape(text):
            name = self.order[info.codepoint]
            t = TransformPen(pen, (s, 0, 0, -s, cx + pos.x_offset * s, y - pos.y_offset * s))
            self.glyphs[name].draw(t)
            cx += pos.x_advance * s + tracking * size
        return pen.getCommands()


DISPLAY = HEAD = BODY = BODY_BOLD = None


def faces():
    global DISPLAY, BODY, BODY_BOLD
    if DISPLAY is None:
        DISPLAY = Face("bricolage", {"wght": 800, "opsz": 96, "wdth": 100})
        BODY = Face("onest", {"wght": 400})
        BODY_BOLD = Face("onest", {"wght": 600})


def text(face, s, size, x, y, fill, anchor="start", tracking=0.0):
    return f'<path fill="{fill}" d="{face.path(s, size, x, y, tracking, anchor)}"/>'


def wordmark(size, x, y, anchor="start", color=CREAM):
    """'shash.builds' with the dot in signal orange."""
    tr = -0.02
    total = DISPLAY.width("shash.builds", size, tr)
    if anchor == "middle":
        x -= total / 2
    elif anchor == "end":
        x -= total
    a = DISPLAY.width("shash", size, tr) + tr * size
    b = DISPLAY.width(".", size, tr) + tr * size
    return (text(DISPLAY, "shash", size, x, y, color, tracking=tr)
            + text(DISPLAY, ".", size, x + a, y, ORANGE, tracking=tr)
            + text(DISPLAY, "builds", size, x + a + b, y, color, tracking=tr))


# ---------- Tab, the mascot ----------
# A browser tab-window with calendar rings on top (he ships on a schedule)
# and an AI spark on its corner. Drawn on a 200 x 200 grid.

TAB_CSS = """
.tab-bob{animation:bob 3.2s ease-in-out infinite}
.tab-eye{transform-box:fill-box;transform-origin:center;animation:blink 4.6s infinite}
.tab-spark{transform-box:fill-box;transform-origin:center;animation:spark 3.2s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
@keyframes blink{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.12)}}
@keyframes spark{0%,100%{transform:rotate(0) scale(1)}50%{transform:rotate(45deg) scale(1.12)}}
@media (prefers-reduced-motion:reduce){.tab-bob,.tab-eye,.tab-spark{animation:none}}
"""


def spark(cx, cy, r, fill=ORANGE, stroke=INK, sw=6, cls=""):
    k = r * 0.16
    d = (f"M{cx},{cy-r} C{cx+k},{cy-k} {cx+k},{cy-k} {cx+r},{cy} "
         f"C{cx+k},{cy+k} {cx+k},{cy+k} {cx},{cy+r} "
         f"C{cx-k},{cy+k} {cx-k},{cy+k} {cx-r},{cy} "
         f"C{cx-k},{cy-k} {cx-k},{cy-k} {cx},{cy-r}Z")
    c = f' class="{cls}"' if cls else ""
    return f'<path{c} d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>'


def tab_group(animated=True, body=CREAM, line=INK):
    bob = ' class="tab-bob"' if animated else ""
    eye = ' class="tab-eye"' if animated else ""
    return f"""<g{bob}>
  <rect x="24" y="40" width="152" height="136" rx="20" fill="{body}"/>
  <path d="M44 40h112a20 20 0 0 1 20 20v14H24V60a20 20 0 0 1 20-20z" fill="{ORANGE}"/>
  <rect x="24" y="40" width="152" height="136" rx="20" fill="none" stroke="{line}" stroke-width="8"/>
  <path d="M24 74h152" stroke="{line}" stroke-width="8"/>
  <circle cx="44" cy="57" r="5" fill="{line}"/><circle cx="60" cy="57" r="5" fill="{line}"/>
  <rect x="88" y="20" width="14" height="38" rx="7" fill="{line}"/>
  <rect x="132" y="20" width="14" height="38" rx="7" fill="{line}"/>
  <ellipse{eye} cx="80" cy="116" rx="9" ry="11" fill="{line}"/>
  <ellipse{eye} cx="120" cy="116" rx="9" ry="11" fill="{line}"/>
  <path d="M84 142q16 14 32 0" fill="none" stroke="{line}" stroke-width="8" stroke-linecap="round"/>
  {spark(176, 38, 30, cls="tab-spark" if animated else "")}
</g>"""


def svg(w, h, body, title, desc, css=""):
    style = f"<style>{css}</style>" if css else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d"><title id="t">{title}</title><desc id="d">{desc}</desc>'
            f"{style}{body}</svg>\n")


def tab(animated=True):
    return svg(200, 200, tab_group(animated), "Tab, the shash.builds mascot",
               "A cream browser window with an orange title bar and two dots, two calendar rings on top, a smiling face and an orange AI spark on its corner.",
               TAB_CSS if animated else "")


def dots(w, h, step=32, color=CREAM, opacity=0.07):
    return (f'<defs><pattern id="g" width="{step}" height="{step}" patternUnits="userSpaceOnUse">'
            f'<circle cx="2" cy="2" r="1.6" fill="{color}"/></pattern></defs>'
            f'<rect width="{w}" height="{h}" fill="url(#g)" opacity="{opacity}"/>')


# ---------- banners ----------

def banner():
    w, h = 1280, 440
    body = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', dots(w, h)]
    body.append(wordmark(128, 72, 210))
    body.append(text(BODY, "One-page websites for US service businesses.", 34, 76, 286, CREAM))
    body.append(text(BODY, "Free Claude skills and web tools, built in public.", 34, 76, 332, MUTED))
    body.append(f'<g transform="translate(900 70) scale(1.5)">{tab_group(True)}</g>')
    body.append(f'<rect y="{h-10}" width="{w}" height="10" fill="{ORANGE}"/>')
    return svg(w, h, "".join(body), "shash.builds",
               "Banner: the shash.builds wordmark next to Tab, the mascot. One-page websites for US service businesses. Free Claude skills and web tools, built in public.",
               TAB_CSS)


def social():
    w, h = 1280, 640
    body = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', dots(w, h)]
    body.append(wordmark(150, 80, 300))
    body.append(text(BODY, "One-page websites for US service businesses.", 38, 84, 384, CREAM))
    body.append(text(BODY, "Free Claude skills and web tools, built in public.", 38, 84, 436, MUTED))
    body.append(text(BODY_BOLD, "github.com/ShashwatBuilds/shash.builds", 28, 84, 548, ORANGE))
    body.append(f'<g transform="translate(910 150) scale(1.6)">{tab_group(False)}</g>')
    body.append(f'<rect y="{h-12}" width="{w}" height="12" fill="{ORANGE}"/>')
    return svg(w, h, "".join(body), "shash.builds social preview",
               "The shash.builds wordmark, the pitch and Tab the mascot on a dark background.")


def profile_header():
    w, h = 1280, 360
    body = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', dots(w, h)]
    body.append(text(DISPLAY, "Shashwat Jain", 104, 72, 170, CREAM, tracking=-0.02))
    body.append(text(BODY, "I build one-page websites for US service businesses.", 32, 76, 236, CREAM))
    body.append(text(BODY, "Free Claude skills too. Built in public at", 32, 76, 282, MUTED))
    x = 76 + BODY.width("Free Claude skills too. Built in public at ", 32)
    body.append(wordmark(32, x, 282))
    body.append(f'<g transform="translate(1000 70) scale(1.15)">{tab_group(True)}</g>')
    body.append(f'<rect y="{h-10}" width="{w}" height="10" fill="{ORANGE}"/>')
    return svg(w, h, "".join(body), "Shashwat Jain, shash.builds",
               "Shashwat Jain builds one-page websites for US service businesses and free Claude skills, in public at shash.builds. Tab the mascot waves from the right.",
               TAB_CSS)


KIND_LABEL = {"skill": "Claude skill", "tool": "Web tool", "template": "Template", "content": "Built in Bed", "research": "Research"}


def header(title, kind, line=""):
    """Per-item README header, same layout for every skill and tool."""
    w, h = 1280, 300
    body = [f'<rect width="{w}" height="{h}" fill="{INK}"/>', dots(w, h)]
    body.append(f'<rect x="72" y="56" width="{BODY_BOLD.width(KIND_LABEL[kind], 24) + 36}" height="44" rx="22" fill="{ORANGE}"/>')
    body.append(text(BODY_BOLD, KIND_LABEL[kind], 24, 90, 86, INK))
    size = 92 if DISPLAY.width(title, 92) < 860 else int(92 * 860 / DISPLAY.width(title, 92))
    body.append(text(DISPLAY, title, size, 70, 196, CREAM, tracking=-0.02))
    if line:
        body.append(text(BODY, line, 28, 74, 250, MUTED))
    body.append(wordmark(30, w - 72, h - 40, anchor="end"))
    body.append(f'<g transform="translate(1020 40) scale(.9)">{tab_group(False)}</g>')
    body.append(f'<rect y="{h-8}" width="{w}" height="8" fill="{ORANGE}"/>')
    return svg(w, h, "".join(body), f"{title}, a shash.builds {KIND_LABEL[kind].lower()}",
               f"Header for {title}. {line}".strip())


# ---------- icons: 48 x 48 orange tiles, readable on light and dark ----------

ICONS = {
    "skill": spark(24, 24, 13, fill=CREAM, stroke=INK, sw=3),
    "tool": f'<path d="M30 12a7 7 0 0 0-8 9L12 31a3 3 0 0 0 4 4l10-10a7 7 0 0 0 9-8l-4 4-4-1-1-4z" fill="{CREAM}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>',
    "template": f'<rect x="11" y="12" width="26" height="24" rx="4" fill="{CREAM}" stroke="{INK}" stroke-width="3"/><path d="M11 19h26M18 19v17" stroke="{INK}" stroke-width="3"/>',
    "video": f'<rect x="10" y="14" width="28" height="20" rx="4" fill="{CREAM}" stroke="{INK}" stroke-width="3"/><path d="M21 19v10l8-5z" fill="{INK}"/>',
    "content": f'<rect x="11" y="13" width="26" height="23" rx="4" fill="{CREAM}" stroke="{INK}" stroke-width="3"/><path d="M11 20h26" stroke="{INK}" stroke-width="3"/><rect x="17" y="9" width="3" height="8" rx="1.5" fill="{INK}"/><rect x="28" y="9" width="3" height="8" rx="1.5" fill="{INK}"/>',
    "research": f'<circle cx="21" cy="21" r="9" fill="{CREAM}" stroke="{INK}" stroke-width="3"/><path d="M28 28l8 8" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>',
    "hire": f'<path d="M12 18h24v16a3 3 0 0 1-3 3H15a3 3 0 0 1-3-3z" fill="{CREAM}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/><path d="M19 18v-3a3 3 0 0 1 3-3h4a3 3 0 0 1 3 3v3M12 25h24" stroke="{INK}" stroke-width="3"/>',
    "log": f'<rect x="12" y="10" width="24" height="28" rx="4" fill="{CREAM}" stroke="{INK}" stroke-width="3"/><path d="M18 18h12M18 24h12M18 30h7" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>',
}
ICON_NAMES = {"skill": "Claude skill", "tool": "Web tool", "template": "Template", "video": "Video",
              "content": "Daily content", "research": "Research", "hire": "Hire", "log": "Build log"}


def icon(name):
    return svg(48, 48, f'<rect width="48" height="48" rx="12" fill="{ORANGE}"/>{ICONS[name]}',
               f"{ICON_NAMES[name]} icon", f"shash.builds {ICON_NAMES[name].lower()} icon")


def build_all():
    out = {
        "banner.svg": banner(), "social-preview.svg": social(), "profile-header.svg": profile_header(),
        "tab.svg": tab(True), "tab-static.svg": tab(False),
        "header-example.svg": header("One-Page Starter", "tool", "Example header. Every skill and tool gets one."),
    }
    out.update({f"icons/{k}.svg": icon(k) for k in ICONS})
    for name, data in out.items():
        (HERE / name).write_text(data)
        print("wrote media/" + name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    hp = sub.add_parser("header", help="make a README header for one skill or tool")
    hp.add_argument("title")
    hp.add_argument("--kind", choices=KIND_LABEL, required=True)
    hp.add_argument("--line", default="", help="one short line under the title")
    hp.add_argument("--out", required=True)
    a = ap.parse_args()
    faces()
    if a.cmd == "header":
        pathlib.Path(a.out).write_text(header(a.title, a.kind, a.line))
        print("wrote", a.out)
    else:
        build_all()
