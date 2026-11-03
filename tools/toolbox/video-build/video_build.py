#!/usr/bin/env python3
"""shash.builds toolbox: video-build.

A day's video.md (plus the voice, face clip and screenshots it names) in, a finished
1080x1920, 30 fps vertical video out: shots cut to the timeline, word-by-word brand captions
burned in, each shot's on-screen text, an optional music bed, loudness at -14 LUFS.

Usage:
  python video_build.py video.md [-o out.mp4] [--words voice.words.json] [--model small]
                        [--stinger tab.mp4] [--music-db -20] [--no-captions] [--dry-run]

video.md format (paths are relative to the video.md folder):

  ---
  date: 2026-11-04
  day: 1
  title: Day 1, short title
  voice: voice.m4a        # the voice track (optional if the face clip has audio)
  face: face.mp4          # the face clip, in sync with the voice from 0:00 (optional)
  music: none             # or: music/bed.mp3 | Track by Artist, CC BY 4.0
  ---
  ## Script
  (plain text; captions come from transcribing the voice, not from this)

  ## Shots
  | at | shot | on-screen text |
  |---|---|---|
  | 0:00 | face | Day 1 |
  | 0:04 | screen: assets/site.png | Built a one-page site in 20 min |

  ## Captions
  burn: yes
  style: brand

Shots: `face`, `screen: FILE` (an image or a video), or `title` (ink background, the
on-screen text large). Each shot runs until the next one's `at`; the last runs to the end.
Captions: the voice is transcribed with the toolbox's transcribe tool (or pass --words).
Needs ffmpeg and Pillow.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
for _p in (HERE / "_shared", HERE.parent / "_shared"):
    if _p.is_dir():
        sys.path.insert(0, str(_p))
        break

W, H, FPS = 1080, 1920, 30
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def log(msg: str) -> None:
    print(f"[video-build] {msg}", file=sys.stderr, flush=True)


# ---------- reading video.md ----------

def parse_time(s: str) -> float:
    s = s.strip()
    if not re.fullmatch(r"\d+(:\d{1,2}){0,2}(\.\d+)?", s):
        raise ValueError(f"bad time {s!r}: use 0:04 or 1:02.5")
    t = 0.0
    for part in s.split(":"):
        t = t * 60 + float(part)
    return t


def parse_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8-sig")
    meta: dict = {}
    body = text
    m = re.match(r"---\s*\n(.*?)\n---\s*\n?(.*)", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            line = re.sub(r"\s+#.*$", "", line).strip()
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip().lower()] = v.strip()
        body = m.group(2)
    sections: dict[str, str] = {}
    for part in re.split(r"^##\s+", body, flags=re.M)[1:]:
        name, _, rest = part.partition("\n")
        sections[name.strip().lower()] = rest
    shots = []
    for line in sections.get("shots", "").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not line.strip().startswith("|") or set(cells[0]) <= set("-: ") or cells[0].lower() == "at":
            continue
        try:
            at = parse_time(cells[0])
        except ValueError as e:
            sys.exit(f"{path.name}, Shots table: {e}")
        kind, _, src = cells[1].partition(":")
        shots.append({"at": at, "kind": kind.strip().lower(), "src": src.strip() or None,
                      "text": cells[2] if len(cells) > 2 else ""})
    for s in shots:
        if s["kind"] not in {"face", "screen", "title"}:
            sys.exit(f"{path.name}: unknown shot {s['kind']!r}; use face, screen: FILE or title")
        if s["kind"] == "screen" and not s["src"]:
            sys.exit(f"{path.name}: a screen shot needs a file, like 'screen: assets/site.png'")
    shots.sort(key=lambda s: s["at"])
    caps = {}
    for line in sections.get("captions", "").splitlines():
        k, _, v = line.partition(":")
        if v:
            caps[k.strip().lower()] = re.sub(r"\s+#.*$", "", v).strip().lower()
    return {"meta": meta, "shots": shots, "captions": caps, "script": sections.get("script", "").strip()}


# ---------- media helpers ----------

def need_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} is not installed. Run the toolbox installer, or get it from https://ffmpeg.org/download.html")


def probe(path: Path) -> dict:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                        "-of", "json", str(path)], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg can't read {path}")
    d = json.loads(r.stdout or "{}")
    types = {s.get("codec_type") for s in d.get("streams", [])}
    try:
        dur = float(d["format"]["duration"])
    except (KeyError, ValueError):
        dur = 0.0
    return {"duration": dur, "audio": "audio" in types, "video": "video" in types}


def ff(args: list[str], cwd: Path | None = None) -> None:
    r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=cwd)
    if r.returncode != 0:
        sys.exit("ffmpeg failed: " + r.stderr.strip()[-600:])


def resolve(base: Path, value: str | None, what: str) -> Path | None:
    if not value or value.lower() == "none":
        return None
    p = (base / value).resolve()
    if not p.is_file():
        sys.exit(f"{what} not found: {p}")
    return p


COVER = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}"
FIT = (f"scale=980:1500:force_original_aspect_ratio=decrease,"
       f"pad={W}:{H}:(ow-iw)/2:(oh-ih)/2-60:color=0x15120f")


def shot_clip(shot: dict, start: float, dur: float, face: Path | None, face_dur: float, out: Path) -> None:
    frames = max(1, round(dur * FPS))
    enc = ["-frames:v", str(frames), "-r", str(FPS), "-an", "-c:v", "libx264", "-preset", "veryfast",
           "-crf", "16", "-pix_fmt", "yuv420p", str(out)]
    if shot["kind"] == "face" and face:
        ss = start % face_dur if face_dur > 0 else 0
        ff(["-stream_loop", "-1", "-ss", f"{ss:.3f}", "-i", str(face), "-vf", f"{COVER},fps={FPS},setsar=1", *enc])
    elif shot["kind"] == "screen":
        src = shot["path"]
        if src.suffix.lower() in IMAGE_EXT:
            # a slow push-in keeps a still from feeling frozen
            zoom = f"scale={W * 2}:-2,zoompan=z='1+0.04*on/{frames}':d={frames}:s={W}x{H}:fps={FPS}"
            ff(["-loop", "1", "-i", str(src), "-vf", f"{FIT},{zoom},setsar=1", *enc])
        else:
            ff(["-stream_loop", "-1", "-i", str(src), "-vf", f"{FIT},fps={FPS},setsar=1", *enc])
    else:  # title, or a face shot with no face clip
        ff(["-f", "lavfi", "-i", f"color=c=0x15120f:s={W}x{H}:r={FPS}", *enc])


# ---------- captions and on-screen text ----------

def caption_groups(words: list[dict], max_words: int = 3, gap: float = 0.5) -> list[list[dict]]:
    """Words in groups of up to max_words, breaking at pauses and sentence ends."""
    groups, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or w["start"] - cur[-1]["end"] > gap or cur[-1]["word"][-1:] in ".?!,"):
            groups.append(cur)
            cur = []
        cur.append(w)
    if cur:
        groups.append(cur)
    return groups


def states(words: list[dict], shots: list[dict], total: float, captions: bool) -> list[tuple[float, float, list[dict], int, str, str]]:
    """Time slices where the overlay doesn't change: (start, end, caption group, highlighted
    word index, shot text, shot kind)."""
    cuts = {0.0, total}
    for s in shots:
        cuts.add(min(s["at"], total))
    groups = caption_groups(words) if captions else []
    for g in groups:
        for w in g:
            cuts.add(min(max(w["start"], 0.0), total))
        cuts.add(min(g[-1]["end"] + 0.35, total))
    times = sorted(cuts)
    out = []
    for a, b in zip(times, times[1:]):
        if b - a < 1 / FPS / 2:
            continue
        mid = (a + b) / 2
        shot = next((s for s in reversed(shots) if s["at"] <= mid), None)
        group, hi = [], -1
        for g in groups:
            if g[0]["start"] <= mid < g[-1]["end"] + 0.35:
                group = g
                hi = max((i for i, w in enumerate(g) if w["start"] <= mid), default=0)
                break
        out.append((a, b, group, hi, shot["text"] if shot else "", shot["kind"] if shot else "face"))
    return out


def draw_overlay(group: list[dict], hi: int, text: str, kind: str, cache: dict):
    from PIL import Image, ImageDraw
    import brand
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ink, cream, orange = brand.rgb(brand.INK), brand.rgb(brand.CREAM), brand.rgb(brand.ORANGE)
    if text and kind == "title":
        f = cache.setdefault("title", brand.font(118, "display", 800))
        lines = brand.wrap(d, text, f, W - 160)
        y = H / 2 - len(lines) * 70
        d.rectangle((80, y - 60, 200, y - 48), fill=orange)
        for line in lines:
            d.text((80, y), line, font=f, fill=cream, anchor="lt")
            y += 140
    elif text:
        f = cache.setdefault("label", brand.font(64, "display", 800))
        lines = brand.wrap(d, text, f, W - 140)[:3]
        y = 210
        for line in lines:
            tw = d.textlength(line, font=f)
            d.rounded_rectangle(((W - tw) / 2 - 34, y - 20, (W + tw) / 2 + 34, y + 76), radius=18, fill=ink + (235,))
            d.text((W / 2, y + 28), line, font=f, fill=cream, anchor="mm")
            y += 104
        d.rectangle((W / 2 - 60, y + 6, W / 2 + 60, y + 16), fill=orange)
    if group:
        f = cache.setdefault("cap", brand.font(78, "display", 800))
        words = [w["word"] for w in group]
        space = d.textlength(" ", font=f)
        widths = [d.textlength(w, font=f) for w in words]
        total = sum(widths) + space * (len(words) - 1)
        if total > W - 160:  # long group: shrink to fit
            f = brand.font(int(78 * (W - 160) / total), "display", 800)
            space = d.textlength(" ", font=f)
            widths = [d.textlength(w, font=f) for w in words]
            total = sum(widths) + space * (len(words) - 1)
        cy = int(H * 0.70)
        d.rounded_rectangle(((W - total) / 2 - 36, cy - 66, (W + total) / 2 + 36, cy + 66), radius=24, fill=ink + (225,))
        x = (W - total) / 2
        for i, (w, wd) in enumerate(zip(words, widths)):
            d.text((x, cy), w, font=f, fill=orange if i == hi else cream, anchor="lm")
            x += wd + space
    return img


def build_overlay_track(slices, tmp: Path) -> Path:
    """One PNG per slice, joined with ffmpeg's concat demuxer into a timed RGBA track."""
    cache: dict = {}
    seen: dict = {}
    lines = []
    for i, (a, b, group, hi, text, kind) in enumerate(slices):
        key = (tuple(w["word"] for w in group), hi, text, kind)
        if key not in seen:
            p = tmp / f"ov_{len(seen):05d}.png"
            draw_overlay(group, hi, text, kind, cache).save(p, compress_level=1)
            seen[key] = p
        lines.append(f"file '{seen[key].name}'\nduration {b - a:.4f}")
    lines.append(f"file '{seen[key].name}'")  # concat demuxer: repeat the last file
    lst = tmp / "overlay.txt"
    lst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lst


# ---------- main ----------

def get_words(args, voice: Path, tmp: Path) -> list[dict]:
    if args.words:
        src = Path(args.words)
    else:
        src = voice.with_name(voice.stem + ".words.json")
        if not src.exists():
            tool = next((p for p in (HERE / "transcribe" / "transcribe.py", HERE.parent / "transcribe" / "transcribe.py")
                         if p.exists()), None)
            if not tool:
                sys.exit("no word timings: run the transcribe tool on the voice first, then pass --words")
            log(f"transcribing {voice.name} with the {args.model} model")
            r = subprocess.run([sys.executable, str(tool), str(voice), "--model", args.model, "--out-dir", str(tmp)],
                               stdout=subprocess.DEVNULL)
            if r.returncode != 0:
                sys.exit("transcription failed; fix that, or pass --words")
            src = tmp / f"{voice.stem}.words.json"
    try:
        data = json.loads(src.read_text(encoding="utf-8"))
        words = data["words"] if isinstance(data, dict) else data
        return [{"word": str(w["word"]), "start": float(w["start"]), "end": float(w["end"])} for w in words]
    except (OSError, ValueError, KeyError, TypeError) as e:
        sys.exit(f"couldn't read word timings from {src}: {e}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video_md")
    ap.add_argument("-o", "--out", help="output file (default: NAME.mp4 next to video.md)")
    ap.add_argument("--words", help="word timings (NAME.words.json from transcribe); default: transcribe the voice")
    ap.add_argument("--model", default="small", help="transcribe model when no --words (small or medium)")
    ap.add_argument("--stinger", help="a short clip added at the end (for example the Tab stinger)")
    ap.add_argument("--music-db", type=float, default=-20, help="music level under the voice, dB (default -20)")
    ap.add_argument("--lufs", type=float, default=-14)
    ap.add_argument("--no-captions", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, render nothing")
    a = ap.parse_args(argv)

    md = Path(a.video_md).resolve()
    if not md.is_file():
        sys.exit(f"not a file: {md}")
    need_ffmpeg()
    spec = parse_md(md)
    meta, base = spec["meta"], md.parent
    voice = resolve(base, meta.get("voice"), "voice")
    face = resolve(base, meta.get("face"), "face clip")
    music_value = meta.get("music", "none")
    music_file, _, credit = music_value.partition("|")
    music = resolve(base, music_file.strip(), "music")
    stinger = resolve(Path.cwd(), a.stinger, "stinger") if a.stinger else None
    face_info = probe(face) if face else {"duration": 0, "audio": False}
    audio_src = voice or (face if face_info["audio"] else None)
    if not audio_src:
        sys.exit("no sound: give a voice file, or a face clip with audio")
    total = probe(audio_src)["duration"]
    if total <= 0:
        sys.exit(f"couldn't read the length of {audio_src}")
    if total > 180:
        log(f"heads up: the voice is {total:.0f} s, longer than a 2-minute video")
    shots = spec["shots"] or [{"at": 0.0, "kind": "face" if face else "title", "src": None, "text": meta.get("title", "")}]
    if shots[0]["at"] > 0:
        shots.insert(0, {**shots[0], "at": 0.0})
    shots = [s for s in shots if s["at"] < total]
    for s in shots:
        if s["kind"] == "screen":
            s["path"] = resolve(base, s["src"], "screen file")
    burn = spec["captions"].get("burn", "yes") != "no" and not a.no_captions

    plan = [{"at": round(s["at"], 2), "until": round(n["at"] if n else total, 2), "shot": s["kind"],
             "file": s.get("src"), "text": s["text"]} for s, n in zip(shots, shots[1:] + [None])]
    out = Path(a.out) if a.out else md.with_name(f"{md.stem}.mp4")
    log(f"{len(plan)} shots, {total:.1f} s, captions {'on' if burn else 'off'}, music {'on' if music else 'off'}")
    if a.dry_run:
        print(json.dumps({"duration": round(total, 2), "shots": plan, "captions": burn,
                          "music": str(music) if music else None, "credit": credit.strip() or None,
                          "out": str(out)}, indent=1))
        return 0

    with tempfile.TemporaryDirectory(prefix="video_build_") as t:
        tmp = Path(t)
        words = get_words(a, audio_src, tmp) if burn else []
        log("cutting shots")
        parts = []
        for i, (s, p) in enumerate(zip(shots, plan)):
            clip = tmp / f"shot_{i:03d}.mp4"
            shot_clip(s, p["at"], p["until"] - p["at"], face, face_info["duration"], clip)
            parts.append(clip)
        (tmp / "shots.txt").write_text("".join(f"file '{p.name}'\n" for p in parts), encoding="utf-8")
        log("drawing captions and on-screen text")
        overlay = build_overlay_track(states(words, shots, total, burn), tmp)
        inputs = ["-f", "concat", "-safe", "0", "-i", "shots.txt", "-f", "concat", "-safe", "0", "-i", overlay.name,
                  "-i", str(audio_src)]
        graph = [f"[1:v]fps={FPS},format=rgba[ov]", f"[0:v][ov]overlay=0:0:format=auto:shortest=0,format=yuv420p[v]"]
        amix = "[2:a]aresample=48000,aformat=channel_layouts=stereo[voice]"
        if music:
            inputs += ["-stream_loop", "-1", "-i", str(music)]
            graph += [amix, f"[3:a]aresample=48000,aformat=channel_layouts=stereo,volume={a.music_db}dB,"
                            f"afade=t=out:st={max(0, total - 2):.2f}:d=2[bed]",
                      "[voice][bed]amix=inputs=2:duration=first:normalize=0[mix]",
                      f"[mix]loudnorm=I={a.lufs}:TP=-1.5:LRA=11,aresample=48000[a]"]
        else:
            graph += [amix, f"[voice]loudnorm=I={a.lufs}:TP=-1.5:LRA=11,aresample=48000[a]"]
        main_out = tmp / "main.mp4" if stinger else out.resolve()
        log("rendering")
        ff([*inputs, "-filter_complex", ";".join(graph), "-map", "[v]", "-map", "[a]", "-t", f"{total:.3f}",
            "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(main_out)], cwd=tmp)
        if stinger:
            log("adding the stinger")
            st = probe(stinger)
            sd = f"{st['duration']:.3f}"
            sa = (f"[1:a]aresample=48000,aformat=channel_layouts=stereo,apad,atrim=0:{sd}[sap]" if st["audio"]
                  else f"anullsrc=r=48000:cl=stereo,atrim=0:{sd}[sap]")
            ff(["-i", str(main_out), "-i", str(stinger), "-filter_complex",
                f"[1:v]{COVER},fps={FPS},setsar=1,format=yuv420p[sv];{sa};"
                f"[0:v][0:a][sv][sap]concat=n=2:v=1:a=1[v][a0];[a0]loudnorm=I={a.lufs}:TP=-1.5:LRA=11,aresample=48000[a]",
                "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out.resolve())])
    if credit.strip():
        Path(f"{out}.credits.txt").write_text(f"Music: {credit.strip()}\n", encoding="utf-8")
        log(f"music credit saved to {out}.credits.txt: put it in the post caption")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
