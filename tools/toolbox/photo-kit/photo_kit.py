#!/usr/bin/env python3
"""shash.builds toolbox: photo-kit.

One photo in; every platform size out, cropped around what matters, compressed, with all
metadata (EXIF, GPS location, camera serials) stripped. Optional background removal.

Usage:
  python photo_kit.py PHOTO [PHOTO ...] [--sizes all|ig-portrait,yt-thumb,...] [--out DIR]
                      [--remove-bg] [--bg-color "#f6efe3"] [--focus auto|center|X,Y]
                      [--format auto|jpg|png|webp] [--quality 82] [--strip-only]

Sizes:
  ig-portrait 1080x1350   ig-story 1080x1920   ig-square 1080x1080
  linkedin 1200x627       linkedin-square 1200x1200
  yt-thumb 1280x720       dribbble 1600x1200   og 1200x630

--remove-bg     cut the subject out with rembg (local model, downloaded once, about 170 MB);
                PNG with transparency, or flat on --bg-color
--focus         auto (default) keeps the busiest or cut-out area in frame; X,Y from 0 to 1
--strip-only    only remove metadata, keep the size
Privacy: metadata is always stripped, there's no switch to keep it. The photo's rotation
from EXIF is applied first, so nothing ends up sideways.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

SIZES = {
    "ig-portrait": (1080, 1350), "ig-story": (1080, 1920), "ig-square": (1080, 1080),
    "linkedin": (1200, 627), "linkedin-square": (1200, 1200),
    "yt-thumb": (1280, 720), "dribbble": (1600, 1200), "og": (1200, 630),
}
GPS_TAG = 0x8825


def log(msg: str) -> None:
    print(f"[photo-kit] {msg}", file=sys.stderr, flush=True)


def need_pillow():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        sys.exit("Pillow is not installed. Run: python -m pip install -r requirements.txt")


def open_clean(path: Path):
    """Open, apply the EXIF rotation, and return a copy with no metadata at all, plus what was found."""
    from PIL import Image, ImageOps, UnidentifiedImageError
    try:
        im = Image.open(path)
        im.load()
    except (UnidentifiedImageError, OSError) as e:
        sys.exit(f"can't open {path} as an image: {e}")
    exif = im.getexif()
    found = {"exif_tags": len(exif), "gps": bool(exif.get(GPS_TAG)) or bool(exif.get_ifd(GPS_TAG)),
             "icc_profile": "icc_profile" in im.info, "other": sorted(k for k in im.info if k not in {"icc_profile", "exif", "dpi"})}
    im = ImageOps.exif_transpose(im)
    mode = "RGBA" if im.mode in {"RGBA", "LA", "PA"} or (im.mode == "P" and "transparency" in im.info) else "RGB"
    if im.mode not in ("RGB", "RGBA"):
        # convert colors to sRGB-ish RGB before dropping the profile
        im = im.convert(mode)
    clean = Image.new(im.mode, im.size)
    clean.paste(im)
    return clean, found


def remove_bg(im):
    try:
        from rembg import remove, new_session
    except ImportError:
        sys.exit("background removal needs rembg: python -m pip install \"rembg[cpu]\"")
    log("removing the background (first run downloads the model once)")
    out = remove(im.convert("RGB"), session=new_session("u2net"))
    return out.convert("RGBA")


def focus_point(im, how: str) -> tuple[float, float]:
    """Where to center crops, as fractions of width and height."""
    if how == "center":
        return 0.5, 0.5
    if how != "auto":
        try:
            x, y = (float(v) for v in how.split(","))
            return min(max(x, 0.0), 1.0), min(max(y, 0.0), 1.0)
        except ValueError:
            sys.exit("--focus takes auto, center, or X,Y between 0 and 1 (like 0.5,0.3)")
    from PIL import ImageFilter
    if im.mode == "RGBA" and im.getchannel("A").getextrema()[0] < 255:
        w = im.getchannel("A").copy()  # a cut-out: center on the subject
        w.thumbnail((128, 128))
        vals = list(w.getdata())
    else:
        # The subject is whatever looks least like the background, and the background is
        # estimated from the photo's border. Robust to gradients, skies and plain walls.
        w = im.convert("RGB").filter(ImageFilter.GaussianBlur(2))
        w.thumbnail((128, 128))
        px = list(w.getdata())
        W_, H_ = w.size
        border = [px[i] for i in range(W_)] + [px[(H_ - 1) * W_ + i] for i in range(W_)] + \
                 [px[r * W_] for r in range(H_)] + [px[r * W_ + W_ - 1] for r in range(H_)]
        bg = [sorted(c[k] for c in border)[len(border) // 2] for k in range(3)]
        dist = [sum((c[k] - bg[k]) ** 2 for k in range(3)) ** 0.5 for c in px]
        cut = sorted(dist)[int(len(dist) * 0.85)]  # keep only the most different 15%
        vals = [d * d if d > cut and d > 25 else 0 for d in dist]
    tot = sx = sy = 0.0
    for i, v in enumerate(vals):
        if v:
            tot += v
            sx += v * (i % w.width)
            sy += v * (i // w.width)
    if tot == 0:
        return 0.5, 0.5
    fx, fy = sx / tot / max(1, w.width - 1), sy / tot / max(1, w.height - 1)
    # pull a little towards the top: in portraits the face sits above the center of mass
    return fx, max(0.0, fy - 0.05)


def fill_crop(im, size: tuple[int, int], focus: tuple[float, float]):
    from PIL import Image
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    rw, rh = max(tw, round(im.width * scale)), max(th, round(im.height * scale))
    big = im.resize((rw, rh), Image.LANCZOS)
    left = min(max(0, round(focus[0] * rw - tw / 2)), rw - tw)
    top = min(max(0, round(focus[1] * rh - th / 2)), rh - th)
    if scale > 1.5:
        log(f"heads up: upscaled {scale:.1f}x for {tw}x{th}; use a bigger photo for a sharp result")
    return big.crop((left, top, left + tw, top + th))


def save(im, path: Path, fmt: str, quality: int) -> Path:
    if fmt == "auto":
        fmt = "png" if im.mode == "RGBA" else "jpg"
    path = path.with_suffix("." + fmt)
    if fmt == "jpg":
        if im.mode == "RGBA":
            sys.exit("JPEG can't keep transparency: use --format png or webp, or --bg-color")
        im.save(path, "JPEG", quality=quality, optimize=True, progressive=True)
    elif fmt == "png":
        im.save(path, "PNG", optimize=True)
    elif fmt == "webp":
        im.save(path, "WEBP", quality=quality, method=6)
    else:
        sys.exit(f"unknown --format {fmt}: use auto, jpg, png or webp")
    return path


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("photos", nargs="+")
    ap.add_argument("--sizes", default="all", help="all, or a comma list of: " + ", ".join(SIZES))
    ap.add_argument("--out", help="output folder (default: PHOTO-kit next to the photo)")
    ap.add_argument("--remove-bg", action="store_true")
    ap.add_argument("--bg-color", help='flat background after --remove-bg, like "#f6efe3"')
    ap.add_argument("--focus", default="auto")
    ap.add_argument("--format", default="auto", choices=["auto", "jpg", "png", "webp"])
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--strip-only", action="store_true", help="only remove metadata, keep the size")
    a = ap.parse_args(argv)
    need_pillow()
    from PIL import Image, ImageColor

    names = list(SIZES) if a.sizes == "all" else [s.strip() for s in a.sizes.split(",") if s.strip()]
    bad = [n for n in names if n not in SIZES]
    if bad:
        sys.exit(f"unknown size {', '.join(bad)}; choose from {', '.join(SIZES)}")
    if not 1 <= a.quality <= 100:
        sys.exit("--quality is 1 to 100")
    report = []
    for p in a.photos:
        src = Path(p)
        if not src.is_file():
            sys.exit(f"not a file: {src}")
        im, found = open_clean(src)
        out_dir = Path(a.out) if a.out else src.with_name(f"{src.stem}-kit")
        out_dir.mkdir(parents=True, exist_ok=True)
        if found["gps"]:
            log(f"{src.name}: had GPS location data; removed")
        files = []
        if a.strip_only:
            fmt = a.format if a.format != "auto" else ("png" if src.suffix.lower() == ".png" or im.mode == "RGBA" else "jpg")
            files.append(save(im, out_dir / f"{src.stem}-clean", fmt, a.quality))
        else:
            if a.remove_bg:
                im = remove_bg(im)
                if a.bg_color:
                    try:
                        bg = Image.new("RGBA", im.size, ImageColor.getrgb(a.bg_color))
                    except ValueError:
                        sys.exit(f"--bg-color {a.bg_color!r} isn't a color; use something like #f6efe3")
                    bg.alpha_composite(im)
                    im = bg.convert("RGB")
                files.append(save(im, out_dir / f"{src.stem}-cutout", a.format, a.quality))
            focus = focus_point(im, a.focus)
            for n in names:
                files.append(save(fill_crop(im, SIZES[n], focus), out_dir / f"{src.stem}-{n}", a.format, a.quality))
        report.append({"photo": src.name, "bytes_in": src.stat().st_size, "metadata_removed": found,
                       "files": [{"file": str(f), "bytes": f.stat().st_size} for f in files]})
        for f in files:
            print(f)
        mine = [r for r in report if Path(r["files"][0]["file"]).parent == out_dir] if a.out else [report[-1]]
        (out_dir / "photo-kit.json").write_text(json.dumps(mine, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
