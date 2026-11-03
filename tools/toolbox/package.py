#!/usr/bin/env python3
"""Package toolbox tools for agensi.io and GitHub Releases. Prepares files only; it never uploads.

    python tools/toolbox/package.py                 # every tool
    python tools/toolbox/package.py transcribe      # one tool
    python tools/toolbox/package.py --check         # validate listings only, no files written
    python tools/toolbox/package.py --no-cover NAME # zip only (what the release workflow runs)

For each tool with an agensi/listing.json it:
  1. checks the listing (title, summary of 160 characters or fewer, tags, price "free", no em dashes);
  2. draws agensi/cover.png (1600x1200) in brand style;
  3. builds dist/toolbox/<tool>-skill.zip: SKILL.md at the top, the tool's scripts, the shared
     brand kit, README, requirements and the MIT license. Zips are not committed (see .gitignore);
     attach them to the tool's GitHub Release and upload to agensi.io once Shashwat approves.
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE / "_shared"))
EM = chr(0x2014)
SKIP = {"agensi", "__pycache__", ".DS_Store"}
TRANSCRIBER = ROOT / "skills/transcriber/skills/transcriber"
# Files from elsewhere in the repo that a tool's zip needs: {tool: {path in zip: source}}.
BUNDLE = {
    "transcribe": {"engine/transcribe.py": TRANSCRIBER / "scripts/transcribe.py",
                   "engine/models.json": TRANSCRIBER / "scripts/models.json",
                   "THIRD_PARTY_NOTICES.md": TRANSCRIBER / "THIRD_PARTY_NOTICES.md"},
}
# video-build carries the transcribe tool (and its engine) for captions.
BUNDLE["video-build"] = {"transcribe/transcribe.py": HERE / "transcribe/transcribe.py",
                         **{f"transcribe/{k}": v for k, v in BUNDLE["transcribe"].items()}}
KEYS = {"title", "summary", "tags", "price", "cover_line", "command"}


def tools() -> list[Path]:
    return sorted(p.parent.parent for p in HERE.glob("*/agensi/listing.json"))


def check(tool: Path) -> list[str]:
    errs = []
    listing = json.loads((tool / "agensi/listing.json").read_text(encoding="utf-8"))
    missing = KEYS - listing.keys()
    if missing:
        errs.append(f"missing {', '.join(sorted(missing))}")
    if len(listing.get("summary", "")) > 160:
        errs.append(f"summary is {len(listing['summary'])} characters (max 160)")
    if listing.get("price") != "free":
        errs.append('price must be "free"')
    if not 3 <= len(listing.get("tags", [])) <= 8:
        errs.append("give 3 to 8 tags")
    desc = tool / "agensi/description.md"
    if not desc.exists():
        errs.append("agensi/description.md missing")
    for f in [tool / "agensi/listing.json", desc, tool / "SKILL.md", tool / "README.md"]:
        if f.exists() and EM in f.read_text(encoding="utf-8"):
            errs.append(f"{f.name}: em dash")
    if not (tool / "SKILL.md").exists():
        errs.append("SKILL.md missing")
    return [f"{tool.name}: {e}" for e in errs]


def cover(tool: Path) -> Path:
    from PIL import Image, ImageDraw
    import brand
    listing = json.loads((tool / "agensi/listing.json").read_text(encoding="utf-8"))
    W, H = 1600, 1200
    img = Image.new("RGB", (W, H), brand.rgb(brand.INK))
    d = ImageDraw.Draw(img)
    for x in range(40, W, 40):  # faint dot grid
        for y in range(40, H, 40):
            d.ellipse((x - 1.5, y - 1.5, x + 1.5, y + 1.5), fill=(38, 34, 30))
    brand.wordmark(d, 110, 150, 54)
    pill = brand.font(30, "body", 600)
    label = "FREE  |  OPEN SOURCE  |  RUNS LOCALLY"
    tw = d.textlength(label, font=pill)
    d.rounded_rectangle((W - 110 - tw - 56, 104, W - 110, 166), radius=31, outline=brand.rgb(brand.ORANGE), width=3)
    d.text((W - 110 - tw / 2 - 28, 135), label, font=pill, fill=brand.rgb(brand.ORANGE), anchor="mm")
    d.rectangle((110, 300, 230, 312), fill=brand.rgb(brand.ORANGE))
    title = brand.font(150, "display", 800)
    d.text((104, 350), listing["title"].split(" by ")[0], font=title, fill=brand.rgb(brand.CREAM), anchor="lt")
    line = brand.font(52, "body", 500)
    y = 560
    for row in brand.wrap(d, listing["cover_line"], line, W - 220)[:2]:
        d.text((110, y), row, font=line, fill=brand.rgb(brand.MUTED), anchor="lt")
        y += 70
    # a terminal card with the one example command
    top = 800
    d.rounded_rectangle((110, top, W - 110, top + 270), radius=24, fill=(30, 26, 22), outline=(60, 54, 47), width=2)
    for i, c in enumerate(("#e8572c", "#b9ad9c", "#6f665b")):
        d.ellipse((150 + i * 34, top + 32, 172 + i * 34, top + 54), fill=brand.rgb(c))
    mono = brand.font(40, "body", 500)
    cmd = "$ " + listing["command"]
    rows = brand.wrap(d, cmd, mono, W - 320)[:3]
    for i, row in enumerate(rows):
        d.text((150, top + 100 + i * 54), row, font=mono, fill=brand.rgb(brand.CREAM), anchor="lt")
    if listing.get("result") and len(rows) < 3:
        d.text((150, top + 100 + len(rows) * 54 + 10), "> " + listing["result"], font=mono,
               fill=brand.rgb(brand.ORANGE), anchor="lt")
    out = tool / "agensi/cover.png"
    img.save(out, optimize=True)
    return out


def build_zip(tool: Path) -> Path:
    dist = ROOT / "dist/toolbox"
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{tool.name}-skill.zip"
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(tool.rglob("*")):
            rel = f.relative_to(tool)
            if f.is_file() and not (set(rel.parts) & SKIP) and f.suffix != ".pyc":
                z.write(f, f"{tool.name}/{rel.as_posix()}")
        for f in sorted((HERE / "_shared").glob("*.py")):
            z.write(f, f"{tool.name}/_shared/{f.name}")
        for inner, src in BUNDLE.get(tool.name, {}).items():
            z.write(src, f"{tool.name}/{inner}")
        z.write(ROOT / "LICENSE", f"{tool.name}/LICENSE.md")
    return out


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    chosen = [t for t in tools() if not args or t.name in args]
    if args and len(chosen) != len(args):
        sys.exit(f"unknown tool; packaged tools: {', '.join(t.name for t in tools())}")
    errs = [e for t in chosen for e in check(t)]
    if errs:
        print("\n".join(errs))
        return 1
    if "--check" in sys.argv:
        print(f"{len(chosen)} listing(s) ok")
        return 0
    for t in chosen:
        if "--no-cover" not in sys.argv:  # CI release builds skip the cover (needs Pillow and fonts)
            print(cover(t).relative_to(ROOT))
        print(build_zip(t).relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
