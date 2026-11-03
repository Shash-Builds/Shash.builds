#!/usr/bin/env python3
"""shash.builds toolbox: transcribe.

Audio or video in, transcript and captions out, on your own computer with local Whisper
(faster-whisper). Nothing is uploaded and no API key is needed.

Usage:
  python transcribe.py FILE [--model small|medium|base|large-v3] [--language auto|en|hi]
                       [--hinglish] [--prompt "names to expect"] [--out-dir DIR]
                       [--model-dir DIR] [--max-chars 42]

Writes, next to FILE (or into --out-dir):
  NAME.txt         plain transcript, one caption line per row
  NAME.srt         captions (SubRip)
  NAME.vtt         captions (WebVTT)
  NAME.words.json  every word with start and end time in seconds
The first run downloads the model once (small is about 470 MB, medium about 1.5 GB) into
the Hugging Face cache. Use --model-dir to point at a copy you already have (offline).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):  # Windows consoles: print Hindi and emoji without crashing
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

# A short Roman-script example steers Whisper to write Hindi in Roman letters and keep
# English words in English, instead of writing everything in Devanagari.
HINGLISH_PROMPT = ("Haan, toh aaj hum baat karenge ki yeh website kaise banti hai. "
                   "Pehle design, phir code, phir launch.")


def log(msg: str) -> None:
    print(f"[transcribe] {msg}", file=sys.stderr, flush=True)


def ts(t: float, sep: str) -> str:
    ms = int(round(max(t, 0) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def to_cues(words: list[dict], max_chars: int = 42, max_s: float = 6.0, gap: float = 0.6) -> list[dict]:
    """Group words into short caption cues: break at pauses, after a sentence end, or
    when a line would get too long. Short cues read well on a phone (reels, shorts)."""
    cues, cur = [], []
    for w in words:
        if cur:
            text = " ".join(x["word"] for x in cur + [w])
            if (w["start"] - cur[-1]["end"] > gap or w["end"] - cur[0]["start"] > max_s
                    or len(text) > max_chars or cur[-1]["word"][-1:] in ".?!"):
                cues.append(cur)
                cur = []
        cur.append(w)
    if cur:
        cues.append(cur)
    return [{"start": c[0]["start"], "end": c[-1]["end"], "text": " ".join(x["word"] for x in c)} for c in cues]


def write_outputs(words: list[dict], stem: Path, meta: dict, max_chars: int) -> list[Path]:
    cues = to_cues(words, max_chars=max_chars)
    paths = [stem.with_suffix(e) for e in (".txt", ".srt", ".vtt")] + [Path(f"{stem}.words.json")]
    paths[0].write_text("\n".join(c["text"] for c in cues) + "\n", encoding="utf-8")
    paths[1].write_text("".join(f"{i}\n{ts(c['start'], ',')} --> {ts(c['end'], ',')}\n{c['text']}\n\n"
                                for i, c in enumerate(cues, 1)), encoding="utf-8")
    paths[2].write_text("WEBVTT\n\n" + "".join(f"{ts(c['start'], '.')} --> {ts(c['end'], '.')}\n{c['text']}\n\n"
                                                for c in cues), encoding="utf-8")
    paths[3].write_text(json.dumps({**meta, "words": words}, ensure_ascii=False, indent=1), encoding="utf-8")
    return paths


def load_model(name: str, model_dir: str | None):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper is not installed. Run: python -m pip install faster-whisper")
    device, compute = "cpu", "int8"
    try:
        import ctranslate2
        if ctranslate2.get_cuda_device_count() > 0:
            device, compute = "cuda", "float16"
    except Exception:  # no CUDA build or no GPU: CPU is fine
        pass
    log(f"loading model {model_dir or name} on {device} (first run downloads it once)")
    return WhisperModel(model_dir or name, device=device, compute_type=compute)


def load_audio(src: Path):
    """16 kHz mono samples. ffmpeg when installed (reads anything), else faster-whisper's
    own decoder (PyAV). PyAV 19 broke that decoder, so requirements.txt pins av<19."""
    import shutil
    import subprocess
    import numpy as np
    if shutil.which("ffmpeg"):
        r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(src), "-f", "f32le",
                            "-ac", "1", "-ar", "16000", "-"], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return np.frombuffer(r.stdout, dtype=np.float32).copy()
        log("ffmpeg could not read the file, trying the built-in decoder")
    from faster_whisper import decode_audio
    try:
        return decode_audio(str(src), sampling_rate=16000)
    except Exception as e:  # noqa: BLE001
        sys.exit(f"could not read audio from {src}: {str(e).splitlines()[0][:200]}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="audio or video file (mp3, wav, m4a, mp4, mov, webm...)")
    ap.add_argument("--model", default="small", help="small (default, fast) or medium (more accurate); base and large-v3 also work")
    ap.add_argument("--language", default="auto", help="auto, en or hi (any Whisper language code works)")
    ap.add_argument("--hinglish", action="store_true", help="Hindi or Hinglish written in Roman letters")
    ap.add_argument("--prompt", help="words or names to expect, for better spelling")
    ap.add_argument("--out-dir", help="where to write the files (default: next to FILE)")
    ap.add_argument("--model-dir", help="a local faster-whisper model folder (works offline)")
    ap.add_argument("--max-chars", type=int, default=42, help="longest caption line (default 42)")
    a = ap.parse_args(argv)

    src = Path(a.file)
    if not src.is_file():
        sys.exit(f"not a file: {src}")
    prompt = a.prompt
    language = None if a.language == "auto" else a.language
    if a.hinglish:
        prompt = HINGLISH_PROMPT + (" " + prompt if prompt else "")
        language = language or "hi"

    model = load_model(a.model, a.model_dir)
    audio = load_audio(src)
    if audio.size == 0:
        sys.exit("the file has no audio")
    segments, info = model.transcribe(audio, language=language, initial_prompt=prompt,
                                      word_timestamps=True, vad_filter=True)
    words = []
    for seg in segments:
        for w in seg.words or []:
            text = w.word.strip()
            if not text:
                continue
            # A piece with no leading space continues the previous word ("one" + "-page").
            if words and not w.word[:1].isspace() and not text[:1].isalnum():
                prev = words[-1]
                prev["word"] += text
                prev["end"] = round(w.end, 3)
                prev["probability"] = round(min(prev["probability"], w.probability), 3)
            else:
                words.append({"word": text, "start": round(w.start, 3), "end": round(w.end, 3),
                              "probability": round(w.probability, 3)})
    if not words:
        sys.exit("no speech found in the file")

    out_dir = Path(a.out_dir) if a.out_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"source": src.name, "language": info.language, "duration": round(info.duration, 3),
            "model": a.model_dir or a.model}
    paths = write_outputs(words, out_dir / src.stem, meta, a.max_chars)
    unsure = sum(1 for w in words if w["probability"] < 0.5)
    log(f"language {info.language}, {info.duration:.1f} s, {len(words)} words, {unsure} unsure")
    for p in paths:
        print(p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
