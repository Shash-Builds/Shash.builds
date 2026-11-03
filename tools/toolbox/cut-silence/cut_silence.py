#!/usr/bin/env python3
"""shash.builds toolbox: cut-silence.

Removes silences (and, with a transcript, "umm" and "uh" fillers) from a face recording or
voice-over, keeping a short pad so speech never sounds clipped. ffmpeg only.

Usage:
  python cut_silence.py INPUT [-o OUTPUT] [--pad 0.15] [--min-silence 0.4] [--threshold -35]
                        [--words NAME.words.json] [--fillers "um,umm,uh,er,ah,hmm"] [--dry-run]

  --words      the NAME.words.json from transcribe: filler words in it are cut too
  --dry-run    print what would be cut, write nothing

Writes OUTPUT (default INPUT_cut.EXT) and OUTPUT.cuts.json: the parts kept and removed, so
captions or edits can be lined up with the new timing.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_FILLERS = "um,umm,ummm,uh,uhh,uhm,er,erm,ah,hmm,hm,mm"


def log(msg: str) -> None:
    print(f"[cut-silence] {msg}", file=sys.stderr, flush=True)


def need_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            sys.exit(f"{tool} is not installed. Run the toolbox installer, or get it from https://ffmpeg.org/download.html")


def probe(path: Path) -> tuple[float, bool]:
    """Duration in seconds, and whether the file has a video stream."""
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
                        "-of", "json", str(path)], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg can't read {path}: {(r.stderr.strip().splitlines() or ['unknown error'])[-1]}")
    info = json.loads(r.stdout or "{}")
    types = {s.get("codec_type") for s in info.get("streams", [])}
    if "audio" not in types:
        sys.exit(f"{path} has no audio track, so there's no silence to find")
    try:
        duration = float(info["format"]["duration"])
    except (KeyError, ValueError):
        sys.exit(f"couldn't read the length of {path}")
    return duration, "video" in types


def detect_silences(path: Path, threshold_db: float, min_silence: float, duration: float) -> list[tuple[float, float]]:
    r = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", str(path), "-vn",
                        "-af", f"silencedetect=noise={threshold_db}dB:d={min_silence}", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    out, start = [], None
    for line in r.stderr.splitlines():
        m = re.search(r"silence_start: (-?[\d.]+)", line)
        if m:
            start = max(0.0, float(m.group(1)))
        m = re.search(r"silence_end: ([\d.]+)", line)
        if m and start is not None:
            out.append((start, float(m.group(1))))
            start = None
    if start is not None:  # silent to the end
        out.append((start, duration))
    return out


def word_spans(words_file: Path, fillers: set[str]):
    """(filler spans, real-word spans) from transcribe's NAME.words.json."""
    try:
        data = json.loads(words_file.read_text(encoding="utf-8"))
        words = data["words"] if isinstance(data, dict) else data
        filler, speech = [], []
        for w in words:
            token = re.sub(r"[^\w]", "", str(w["word"]).lower())
            (filler if token in fillers else speech).append((float(w["start"]), float(w["end"])))
        return filler, speech
    except (OSError, ValueError, KeyError, TypeError) as e:
        sys.exit(f"couldn't read word timings from {words_file}: {e}. Use the .words.json from transcribe.")


def plan(duration: float, removals: list[tuple[float, float]], pad: float, min_cut: float = 0.1,
         speech: list[tuple[float, float]] | None = None):
    """Merge what to remove, give speech `pad` seconds on each side, return (keep, removed).
    With word timings (`speech`), two cuts with no real word between them become one, so
    the tail of an "umm" that Whisper timed short doesn't survive as a sliver."""
    spans = sorted((max(0.0, a), min(duration, b)) for a, b in removals if b > a)

    def no_word_between(a: float, b: float) -> bool:
        return speech is not None and not any(s < b and e > a for s, e in speech)

    merged: list[list[float]] = []
    for a, b in spans:
        if merged and (a <= merged[-1][1] or no_word_between(merged[-1][1], a)):
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    removed = []
    for a, b in merged:
        a2 = a + pad if a > 0 else 0.0  # no pad needed before the first word
        b2 = b - pad if b < duration else duration
        if b2 - a2 >= min_cut:
            removed.append((round(a2, 3), round(b2, 3)))
    keep, t = [], 0.0
    for a, b in removed:
        if a > t:
            keep.append((round(t, 3), a))
        t = b
    if t < duration:
        keep.append((round(t, 3), round(duration, 3)))
    return keep, removed


def render(src: Path, dst: Path, keep: list[tuple[float, float]], has_video: bool) -> None:
    expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep)
    parts = [f"[0:a]aselect='{expr}',asetpts=N/SR/TB[a]"]
    maps = ["-map", "[a]"]
    if has_video:
        parts.insert(0, f"[0:v]select='{expr}',setpts=N/FRAME_RATE/TB[v]")
        maps = ["-map", "[v]"] + maps
    cmd = ["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(src), "-filter_complex", ";".join(parts), *maps]
    if has_video:
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k"]
        if dst.suffix.lower() in {".mp4", ".mov", ".m4v"}:
            cmd += ["-movflags", "+faststart"]
    r = subprocess.run(cmd + [str(dst)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit("ffmpeg failed: " + (r.stderr.strip().splitlines() or ["unknown error"])[-1])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input")
    ap.add_argument("-o", "--output")
    ap.add_argument("--pad", type=float, default=0.15, help="seconds kept around speech (default 0.15)")
    ap.add_argument("--min-silence", type=float, default=0.4, help="shortest pause to cut, seconds (default 0.4)")
    ap.add_argument("--threshold", type=float, default=-35, help="silence level in dB (default -35; noisy room: -30)")
    ap.add_argument("--words", help="NAME.words.json from transcribe, to also cut filler words")
    ap.add_argument("--fillers", default=DEFAULT_FILLERS, help="comma-separated filler words to cut")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    need_ffmpeg()
    src = Path(a.input)
    if not src.is_file():
        sys.exit(f"not a file: {src}")
    if a.pad < 0 or a.min_silence <= 0:
        sys.exit("--pad must be 0 or more and --min-silence more than 0")
    duration, has_video = probe(src)
    removals = detect_silences(src, a.threshold, a.min_silence, duration)
    n_silence = len(removals)
    speech = None
    if a.words:
        fillers = {f.strip().lower() for f in a.fillers.split(",") if f.strip()}
        filler, speech = word_spans(Path(a.words), fillers)
        removals += filler
    keep, removed = plan(duration, removals, a.pad, speech=speech)
    if not keep:
        sys.exit("the whole file is silent at this threshold; try --threshold -45")
    kept_s = sum(b - a for a, b in keep)
    summary = {"input": src.name, "duration": round(duration, 3), "new_duration": round(kept_s, 3),
               "removed_seconds": round(duration - kept_s, 3), "silences_found": n_silence,
               "fillers_found": len(removals) - n_silence, "pad": a.pad,
               "keep": [list(k) for k in keep], "removed": [list(r) for r in removed]}
    log(f"{duration:.1f} s to {kept_s:.1f} s: {len(removed)} cuts "
        f"({n_silence} silences, {len(removals) - n_silence} fillers)")
    if a.dry_run:
        print(json.dumps(summary, indent=1))
        return 0
    dst = Path(a.output) if a.output else src.with_name(f"{src.stem}_cut{src.suffix}")
    if dst.resolve() == src.resolve():
        sys.exit("output would overwrite the input; pick another name with -o")
    if not removed:
        log("nothing to cut; copying the file as is")
        shutil.copyfile(src, dst)
    else:
        render(src, dst, keep, has_video)
    Path(f"{dst}.cuts.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
