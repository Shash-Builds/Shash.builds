#!/usr/bin/env python3
"""shash.builds toolbox: transcribe.

Audio or video in, transcript and captions out, on your own computer with local Whisper
(faster-whisper). Nothing is uploaded and no API key is needed.

This is the command-line front end of the shash.builds Transcriber skill: the engine is
skills/transcriber/skills/transcriber/scripts/transcribe.py (or engine/ next to this file in
the skill zip). It adds toolbox defaults (short reel-sized captions, model choice by name)
and a flat word list for cut-silence and video-build.

Usage:
  python transcribe.py FILE [--model small|medium|base|large-v3] [--language auto|en|hi]
                       [--hinglish] [--prompt "names to expect"] [--out-dir DIR]
                       [--model-dir DIR] [--max-chars 42]

Writes, next to FILE (or into --out-dir):
  NAME.txt         plain transcript, one caption line per row
  NAME.srt         captions (SubRip)
  NAME.vtt         captions (WebVTT)
  NAME.json        the engine's segments with word timings
  NAME.words.json  every word with start and end time in seconds
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows consoles: print Hindi and emoji without crashing
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

HERE = Path(__file__).resolve().parent
ENGINES = [HERE / "engine" / "transcribe.py",
           HERE.parent.parent.parent / "skills/transcriber/skills/transcriber/scripts/transcribe.py"]


def engine() -> Path:
    for p in ENGINES:
        if p.is_file():
            return p
    sys.exit("the transcriber engine is missing; reinstall the toolbox or the transcribe skill zip")


def flat_words(engine_json: Path) -> dict:
    data = json.loads(engine_json.read_text(encoding="utf-8"))
    words = [w for s in data.get("segments", []) for w in s.get("words", [])]
    return {k: data.get(k) for k in ("language", "duration", "model")} | {"words": words}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="audio or video file (mp3, wav, m4a, mp4, mov, webm...)")
    ap.add_argument("--model", default="small", help="small (default, fast) or medium (more accurate); base and large-v3 also work")
    ap.add_argument("--language", default="auto", help="auto, en or hi (any Whisper language code works)")
    ap.add_argument("--hinglish", action="store_true", help="Hindi or Hinglish written in Roman letters")
    ap.add_argument("--prompt", help="words or names to expect, for better spelling")
    ap.add_argument("--out-dir", help="where to write the files (default: next to FILE)")
    ap.add_argument("--model-dir", help="a local faster-whisper model folder (works offline)")
    ap.add_argument("--max-chars", type=int, default=42, help="longest caption line (default 42, reel-sized)")
    a = ap.parse_args(argv)

    src = Path(a.file)
    if not src.is_file():
        sys.exit(f"not a file: {src}")
    out_dir = Path(a.out_dir) if a.out_dir else src.parent
    cmd = [sys.executable, str(engine()), str(src), "--size", a.model, "--language", a.language,
           "--out-dir", str(out_dir), "--max-chars", str(a.max_chars)]
    if a.hinglish:
        cmd.append("--hinglish")
    if a.prompt:
        cmd += ["--prompt", a.prompt]
    if a.model_dir:
        cmd += ["--model-dir", a.model_dir]
    r = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.stdout.write(r.stdout)
        return r.returncode
    engine_json = out_dir / f"{src.stem}.json"
    words = out_dir / f"{src.stem}.words.json"
    words.write_text(json.dumps(flat_words(engine_json), ensure_ascii=False, indent=1), encoding="utf-8")
    for ext in ("txt", "srt", "vtt", "json", "words.json"):
        print(out_dir / f"{src.stem}.{ext}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
