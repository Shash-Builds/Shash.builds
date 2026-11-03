"""shash.builds brand kit for the toolbox: colors and fonts, shared by every tool that draws.

Fonts are SIL Open Font License 1.1 (Bricolage Grotesque by Mathieu Triay; Onest by Dmitri
Voloshin and Andrey Kudryavtsev). They download once into ~/.cache/shashbuilds-fonts. If
there is no internet, the tools fall back to a system font and say so.
"""
from __future__ import annotations

import os
import sys
import urllib.request
from pathlib import Path

ORANGE, INK, CREAM, MUTED = "#e8572c", "#15120f", "#f6efe3", "#b9ad9c"

FONT_URLS = {
    "display": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf",
    "body": "https://cdn.jsdelivr.net/gh/google/fonts@main/ofl/onest/Onest%5Bwght%5D.ttf",
}
CACHE = Path(os.environ.get("SHASHBUILDS_FONTS", Path.home() / ".cache" / "shashbuilds-fonts"))
FALLBACKS = ["DejaVuSans-Bold.ttf", "arialbd.ttf", "Arial Bold.ttf", "Helvetica.ttc", "DejaVuSans.ttf", "arial.ttf"]


def rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def font_file(kind: str = "display") -> Path | None:
    """Path to the brand font, downloading it once. None if it can't be fetched."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{kind}.ttf"
    if not path.exists():
        try:
            urllib.request.urlretrieve(FONT_URLS[kind], path)
        except Exception as e:  # noqa: BLE001 - offline is fine, we fall back
            print(f"[brand] could not download the {kind} font ({e}); using a system font", file=sys.stderr)
            if path.exists():
                path.unlink()
            return None
    return path


def font(size: int, kind: str = "display", weight: int = 700):
    """A Pillow font at the given size and weight (variable fonts set to that weight)."""
    from PIL import ImageFont
    path = font_file(kind)
    if path:
        f = ImageFont.truetype(str(path), size)
        try:
            axes = f.get_variation_axes()
            values = []
            for ax in axes:
                name = ax.get("name", b"")
                name = name.decode() if isinstance(name, bytes) else str(name)
                if name.lower().startswith("weight"):
                    values.append(max(ax["minimum"], min(ax["maximum"], weight)))
                elif name.lower().startswith("optical"):
                    values.append(max(ax["minimum"], min(ax["maximum"], size)))
                else:
                    values.append(ax.get("default", ax["minimum"]))
            f.set_variation_by_axes(values)
        except Exception:  # noqa: BLE001 - static font or no FreeType variation support
            pass
        return f
    for name in FALLBACKS:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


def wrap(draw, text: str, fnt, max_width: int) -> list[str]:
    """Greedy word wrap to max_width pixels."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wordmark(draw, x: int, y: int, size: int, color: str = CREAM, anchor: str = "ls") -> None:
    """Draw "shash.builds" with the dot in orange."""
    f = font(size, "display", 800)
    parts = [("shash", color), (".", ORANGE), ("builds", color)]
    total = sum(draw.textlength(t, font=f) for t, _ in parts)
    if anchor[0] == "m":
        x -= total / 2
    elif anchor[0] == "r":
        x -= total
    for t, c in parts:
        draw.text((x, y), t, font=f, fill=c, anchor="l" + anchor[1])
        x += draw.textlength(t, font=f)
