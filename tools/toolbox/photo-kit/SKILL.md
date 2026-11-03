---
name: photo-kit
description: Turn one photo into every platform size (Instagram, LinkedIn, YouTube thumbnail, Dribbble, OG image), cropped around the subject, compressed, with EXIF and GPS location always stripped; optional local background removal. Use for "resize this for Instagram", "remove the background", "strip the location from this photo".
---

The script sits next to this SKILL.md (in Claude Code: `${CLAUDE_SKILL_DIR}/photo_kit.py`).
It needs Pillow; `--remove-bg` also needs rembg (`python -m pip install -r requirements.txt`).

1. Ask which platforms the photo is for, or use `--sizes all`. Sizes: ig-portrait, ig-story,
   ig-square, linkedin, linkedin-square, yt-thumb, dribbble, og.
2. Run `python photo_kit.py PHOTO --sizes ig-portrait,yt-thumb --out OUTDIR`. Add
   `--remove-bg` for a cut-out (PNG with transparency) and `--bg-color "#f6efe3"` for a flat
   background. Use `--strip-only` to clean metadata without resizing.
3. Look at every crop. If the subject is cut off, run again with `--focus X,Y` (0 to 1,
   where the subject is) and say so.
4. Tell the user what metadata was removed (photo-kit.json in OUTDIR lists it, including
   whether GPS location was found). Metadata is always removed; never offer to keep it.

The first `--remove-bg` run downloads the model once (about 170 MB).
