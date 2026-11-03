#!/usr/bin/env python3
"""shash.builds toolbox: repurpose.

One transcript in; a LinkedIn post, an Instagram caption with 3 hashtags, an X thread and a
YouTube title, description and chapters out. Human tone, no em dashes.

No API key needed. Three ways to run it:
  python repurpose.py prompt TRANSCRIPT [--topic "..."] [--out DIR]
      writes NAME.repurpose-prompt.md: paste it into any chat model (Claude, or any other),
      save the answer as NAME.repurpose.md, then run `check` on it.
  python repurpose.py prompt TRANSCRIPT --ollama llama3.1
      also runs the prompt on a local Ollama model (free, open source) if one is running,
      writes NAME.repurpose.md and checks it.
  python repurpose.py check NAME.repurpose.md
      checks an answer: every section there, platform limits, exactly 3 hashtags, chapters
      that YouTube accepts, no em dashes. Exits 1 with a list of fixes.

TRANSCRIPT can be the .txt, .srt, .vtt, .json or .words.json from the transcribe tool.
With timings (srt, vtt, json) the prompt includes timestamped chapter candidates.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

EM, EN = chr(0x2014), chr(0x2013)
SECTIONS = ["LinkedIn", "Instagram", "X thread", "YouTube"]
LIMITS = {"linkedin": 3000, "instagram": 2200, "tweet": 280, "yt_title": 100, "yt_description": 5000}
# Phrases that make writing sound machine-made. Kept short on purpose: the humanizer skill has the full list.
STOCK = ["delve", "game-changer", "game changer", "in today's fast-paced", "unlock the power", "elevate your",
         "let's dive in", "dive into", "in the ever-evolving", "it's not just", "here's the thing",
         "buckle up", "a testament to", "navigate the", "landscape of", "seamless", "harness the power",
         "revolutionize", "unleash", "supercharge"]

RULES = """Rules for every piece:
- Write like a person talking to a friend: short sentences, plain words, contractions.
- Use only facts, numbers and names that are in the transcript. Never invent results, clients or quotes.
- No em dashes and no en dashes. Use a comma, a colon, a full stop or "and".
- No hype words: delve, game-changer, unlock, elevate, seamless, supercharge, revolutionize.
- No emoji walls. At most two emoji in the whole Instagram caption, none elsewhere.
- Open each piece with the most specific, surprising line from the transcript, not with a greeting."""

FORMAT = """Answer in exactly this format (Markdown, these four headings, nothing before or after):

## LinkedIn
(150 to 250 words. First line under 60 characters so it shows before "see more". Short paragraphs. End with one question.)

## Instagram
(80 to 150 words. First line is the hook. Last line: exactly 3 hashtags, nothing else on it.)

## X thread
1/ (each post under 280 characters, 4 to 7 posts, numbered 1/ 2/ 3/ on their own lines)

## YouTube
Title: (under 70 characters, says what the viewer gets)
Description: (2 to 4 sentences, then a blank line)
Chapters:
00:00 (first chapter, always 00:00)
(at least 3 chapters, each at least 10 seconds after the one before, times from the transcript)"""


# ---------- reading transcripts ----------

def parse_ts(s: str) -> float:
    s = s.strip().replace(",", ".")
    t = 0.0
    for part in s.split(":"):
        t = t * 60 + float(part)
    return t


def load_transcript(path: Path) -> tuple[str, list[tuple[float, str]]]:
    """(plain text, [(start seconds, line)]). The list is empty when there are no timings."""
    raw = path.read_text(encoding="utf-8-sig", errors="replace")
    suffix = path.suffix.lower()
    cues: list[tuple[float, str]] = []
    if suffix == ".json":
        data = json.loads(raw)
        if isinstance(data, dict) and data.get("segments"):
            cues = [(float(s["start"]), str(s["text"]).strip()) for s in data["segments"]]
        elif isinstance(data, dict) and data.get("words"):
            line, start = [], None
            for w in data["words"]:
                start = float(w["start"]) if start is None else start
                line.append(str(w["word"]))
                if str(w["word"])[-1:] in ".?!" or len(line) >= 14:
                    cues.append((start, " ".join(line)))
                    line, start = [], None
            if line:
                cues.append((start or 0.0, " ".join(line)))
        else:
            raise ValueError("a .json transcript needs 'segments' or 'words' (from the transcribe tool)")
    elif suffix in {".srt", ".vtt"}:
        for block in re.split(r"\n\s*\n", raw.replace("\r", "")):
            lines = [x for x in block.strip().splitlines() if x.strip()]
            for i, x in enumerate(lines):
                if "-->" in x:
                    text = " ".join(lines[i + 1:]).strip()
                    text = re.sub(r"<[^>]+>", "", text)
                    if text:
                        cues.append((parse_ts(x.split("-->")[0].strip().split(" ")[0]), text))
                    break
    else:
        text = raw.strip()
        return text, []
    return " ".join(c[1] for c in cues), cues


def fmt(t: float) -> str:
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def timed_lines(cues: list[tuple[float, str]], every: float = 8.0) -> str:
    """The transcript with a timestamp at least every few seconds, for chapter picking."""
    out, last = [], -every
    for start, text in cues:
        if start - last >= every:
            out.append(f"[{fmt(start)}] {text}")
            last = start
        else:
            out[-1] += " " + text
    return "\n".join(out)


def build_prompt(text: str, cues: list[tuple[float, str]], topic: str | None) -> str:
    body = timed_lines(cues) if cues else text
    duration = f" The video is about {fmt(cues[-1][0])} long." if cues else ""
    chapters = ("Pick chapter times from the [mm:ss] marks." if cues else
                "There are no timings in this transcript, so leave Chapters as 00:00 Intro and add a note to time the rest.")
    return f"""# Repurpose this video

You're repurposing one short video by a founder into four posts.{duration}
{f"Topic: {topic}" if topic else ""}

{RULES}

{chapters}

{FORMAT}

## Transcript

{body}
"""


# ---------- checking answers ----------

def split_sections(md: str) -> dict[str, str]:
    parts = re.split(r"^##\s+(.+?)\s*$", md, flags=re.M)
    return {parts[i].strip().lower(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def check(md: str) -> list[str]:
    errs = []
    if EM in md or EN in md:
        n = md.count(EM) + md.count(EN)
        errs.append(f"{n} em or en dash(es): rewrite with a comma, colon or full stop")
    low = md.lower()
    for phrase in STOCK:
        if phrase in low:
            errs.append(f'stock phrase "{phrase}": say it plainly')
    sec = split_sections(md)
    for name in SECTIONS:
        if name.lower() not in sec:
            errs.append(f"missing section: ## {name}")
    li = sec.get("linkedin", "")
    if li:
        if len(li) > LIMITS["linkedin"]:
            errs.append(f"LinkedIn: {len(li)} characters, limit {LIMITS['linkedin']}")
        first = li.splitlines()[0]
        if len(first) > 60:
            errs.append(f"LinkedIn: first line is {len(first)} characters; keep it under 60 so it shows before 'see more'")
    ig = sec.get("instagram", "")
    if ig:
        if len(ig) > LIMITS["instagram"]:
            errs.append(f"Instagram: {len(ig)} characters, limit {LIMITS['instagram']}")
        tags = re.findall(r"(?<!\w)#\w+", ig)
        if len(tags) != 3:
            errs.append(f"Instagram: {len(tags)} hashtags, need exactly 3")
        last = ig.strip().splitlines()[-1]
        if tags and not all(w.startswith("#") for w in last.split()):
            errs.append("Instagram: put the 3 hashtags alone on the last line")
    xt = sec.get("x thread", "")
    if xt:
        posts = [p.strip() for p in re.split(r"(?m)^\s*\d+/\s*", xt) if p.strip()]
        if not 2 <= len(posts) <= 10:
            errs.append(f"X thread: {len(posts)} posts; number them 1/ 2/ 3/ on their own lines")
        for i, p in enumerate(posts, 1):
            if len(p) + len(f"{i}/ ") > LIMITS["tweet"]:
                errs.append(f"X thread: post {i} is {len(p) + len(f'{i}/ ')} characters, limit {LIMITS['tweet']}")
    yt = sec.get("youtube", "")
    if yt:
        m = re.search(r"(?im)^title:\s*(.+)$", yt)
        if not m:
            errs.append("YouTube: no 'Title:' line")
        elif len(m.group(1).strip()) > LIMITS["yt_title"]:
            errs.append(f"YouTube: title is {len(m.group(1).strip())} characters, limit {LIMITS['yt_title']}")
        if "<" in yt or ">" in yt:
            errs.append("YouTube: remove < and >, YouTube rejects them in descriptions")
        if len(yt) > LIMITS["yt_description"]:
            errs.append(f"YouTube: description is {len(yt)} characters, limit {LIMITS['yt_description']}")
        times = [parse_ts(t) for t in re.findall(r"(?m)^\s*((?:\d+:)?\d{1,2}:\d{2})\s+\S", yt)]
        if not times:
            errs.append("YouTube: no chapters (lines like '00:00 Intro')")
        else:
            if times[0] != 0:
                errs.append("YouTube: the first chapter must be 00:00")
            if len(times) < 3:
                errs.append(f"YouTube: {len(times)} chapter(s); YouTube needs at least 3")
            for a, b in zip(times, times[1:]):
                if b - a < 10:
                    errs.append(f"YouTube: chapters at {fmt(a)} and {fmt(b)} are under 10 seconds apart")
    return errs


# ---------- optional local model ----------

def ollama(model: str, prompt: str, host: str) -> str | None:
    req = urllib.request.Request(f"{host.rstrip('/')}/api/generate", method="POST",
                                 data=json.dumps({"model": model, "prompt": prompt, "stream": False}).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            return json.loads(r.read().decode("utf-8")).get("response", "").strip() or None
    except (urllib.error.URLError, OSError, ValueError) as e:
        print(f"[repurpose] Ollama not reachable at {host} ({e}); use the prompt file instead", file=sys.stderr)
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prompt", help="write the ready prompt (and run it on Ollama if asked)")
    p.add_argument("transcript")
    p.add_argument("--topic", help="one line on what the video is about")
    p.add_argument("--out", help="folder for the files (default: next to the transcript)")
    p.add_argument("--ollama", metavar="MODEL", help="run the prompt on this local Ollama model")
    p.add_argument("--ollama-host", default="http://localhost:11434")
    c = sub.add_parser("check", help="check an answer file")
    c.add_argument("answer")
    a = ap.parse_args(argv)

    if a.cmd == "check":
        path = Path(a.answer)
        if not path.is_file():
            sys.exit(f"not a file: {path}")
        errs = check(path.read_text(encoding="utf-8-sig", errors="replace"))
        print("\n".join(f"- {e}" for e in errs) if errs else "ok: all four pieces pass")
        return 1 if errs else 0

    src = Path(a.transcript)
    if not src.is_file():
        sys.exit(f"not a file: {src}")
    try:
        text, cues = load_transcript(src)
    except (ValueError, KeyError, TypeError) as e:
        sys.exit(f"couldn't read {src}: {e}")
    if len(text.split()) < 20:
        sys.exit(f"{src} has only {len(text.split())} words; repurposing needs a real transcript")
    out_dir = Path(a.out) if a.out else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.name.split(".")[0]
    prompt = build_prompt(text, cues, a.topic)
    prompt_file = out_dir / f"{stem}.repurpose-prompt.md"
    prompt_file.write_text(prompt, encoding="utf-8")
    print(prompt_file)
    if a.ollama:
        answer = ollama(a.ollama, prompt, a.ollama_host)
        if answer:
            ans_file = out_dir / f"{stem}.repurpose.md"
            ans_file.write_text(answer + "\n", encoding="utf-8")
            print(ans_file)
            errs = check(answer)
            print("\n".join(f"- {e}" for e in errs) if errs else "ok: all four pieces pass")
            return 1 if errs else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
