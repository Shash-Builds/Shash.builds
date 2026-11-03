"""Tests for tools/toolbox, run by tests/run_tests.py (kept in their own file to keep merges easy).

Fast checks: structure, SKILL.md frontmatter, listings. Script checks run each tool on
synthetic inputs built here; a tool whose heavy dependency (a Whisper model, rembg) isn't
installed is tested through its pure functions or reported as SKIP.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLBOX = ROOT / "tools/toolbox"


def load(tool: str, script: str):
    spec = importlib.util.spec_from_file_location(f"tb_{tool}", TOOLBOX / tool / script)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def tool_dirs() -> list[Path]:
    return sorted(p for p in TOOLBOX.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def register(test, frontmatter, run, need, tmp: Path, fast: bool, Skip=Exception) -> None:
    @test
    def test_toolbox_tools_have_readme_skill_requirements_and_listing():
        assert tool_dirs(), "no toolbox tools found"
        for d in tool_dirs():
            for f in ("README.md", "SKILL.md", "agensi/listing.json", "agensi/description.md", "agensi/cover.png"):
                assert (d / f).exists(), f"{d.name}: missing {f}"
            fm = frontmatter(d / "SKILL.md")
            assert set(fm) == {"name", "description"}, f"{d.name}: SKILL.md frontmatter must be name and description only"
            assert fm["name"] == d.name, f"{d.name}: SKILL.md name is {fm['name']}"
            assert len(fm["description"].split()) <= 55, f"{d.name}: SKILL.md description over 55 words"
            readme = (d / "README.md").read_text(encoding="utf-8")
            assert "## Licenses" in readme, f"{d.name}: README needs a Licenses section"
            assert "Windows" in readme, f"{d.name}: README needs the Windows command"
            listed = (TOOLBOX / "README.md").read_text(encoding="utf-8")
            assert f"[{d.name}]({d.name})" in listed, f"{d.name}: not linked from the toolbox README"

    @test
    def test_toolbox_listings_pass_the_packager_check():
        run([sys.executable, str(TOOLBOX / "package.py"), "--check"])

    @test
    def test_toolbox_covers_are_1600_by_1200():
        from PIL import Image
        for d in tool_dirs():
            with Image.open(d / "agensi/cover.png") as im:
                assert im.size == (1600, 1200), f"{d.name}: cover is {im.size}"

    @test
    def test_toolbox_transcribe_writes_captions_from_word_timings():
        t = load("transcribe", "transcribe.py")
        words = [{"word": w, "start": i * 0.3, "end": i * 0.3 + 0.25, "probability": 0.9}
                 for i, w in enumerate("Hello and welcome. Today we build a one-page site".split())]
        words[-1]["start"] += 2  # a long pause before the last word starts a new cue
        words[-1]["end"] += 2
        out = tmp / "transcribe"
        out.mkdir()
        paths = t.write_outputs(words, out / "demo", {"language": "en"}, 42)
        srt = (out / "demo.srt").read_text(encoding="utf-8")
        assert srt.startswith("1\n00:00:00,000 --> "), srt[:60]
        lines = (out / "demo.txt").read_text(encoding="utf-8").splitlines()
        assert lines[0] == "Hello and welcome.", lines
        assert lines[-1] == "site", lines
        assert (out / "demo.vtt").read_text(encoding="utf-8").startswith("WEBVTT\n\n00:00:00.000")
        data = json.loads((out / "demo.words.json").read_text(encoding="utf-8"))
        assert len(data["words"]) == len(words) and len(paths) == 4
        assert t.ts(3661.5, ",") == "01:01:01,500"

    @test
    def test_toolbox_transcribe_refuses_a_missing_file_plainly():
        r = subprocess.run([sys.executable, str(TOOLBOX / "transcribe/transcribe.py"), str(tmp / "nope.wav")],
                           capture_output=True, text=True)
        assert r.returncode != 0 and "not a file" in r.stderr and "Traceback" not in r.stderr, r.stderr

    @test
    def test_toolbox_cut_silence_plans_cuts_with_pad_and_bridges_fillers():
        t = load("cut-silence", "cut_silence.py")
        keep, removed = t.plan(10.0, [(2.0, 4.0), (8.0, 10.0)], 0.15)
        assert removed == [(2.15, 3.85), (8.15, 10.0)], removed
        assert keep == [(0.0, 2.15), (3.85, 8.15)], keep
        # silence, filler, silence with no real word between them: one cut
        keep, removed = t.plan(10.0, [(2.0, 3.0), (3.2, 3.5), (3.9, 5.0)], 0.15, speech=[(0.5, 1.9), (5.1, 6.0)])
        assert removed == [(2.15, 4.85)], removed
        # a real word between two cuts is kept
        keep, removed = t.plan(10.0, [(2.0, 3.0), (3.9, 5.0)], 0.15, speech=[(3.2, 3.6)])
        assert len(removed) == 2, removed
        assert t.plan(1.0, [(0.0, 0.05)], 0.15)[1] == [], "cuts shorter than the pads are skipped"

    @test
    def test_toolbox_cut_silence_cuts_a_real_video():
        if fast:
            raise Skip("full mode only")
        need("ffmpeg", "ffprobe")
        src = tmp / "tone_gaps.mp4"
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=320x240:r=25:d=5",
             "-f", "lavfi", "-i", "sine=f=440:d=5",
             "-filter_complex", "[1]volume='if(between(t,1.5,3.5),0,1)':eval=frame[a]",
             "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", str(src)])
        out = tmp / "cut.mp4"
        run([sys.executable, str(TOOLBOX / "cut-silence/cut_silence.py"), str(src), "-o", str(out)])
        r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)])
        assert 2.8 < float(r.stdout) < 3.6, f"expected about 3.3 s, got {r.stdout.strip()}"
        cuts = json.loads(Path(f"{out}.cuts.json").read_text(encoding="utf-8"))
        assert cuts["silences_found"] == 1 and len(cuts["removed"]) == 1, cuts
        r = subprocess.run([sys.executable, str(TOOLBOX / "cut-silence/cut_silence.py"), str(src), "-o", str(src)],
                           capture_output=True, text=True)
        assert r.returncode != 0 and "overwrite" in r.stderr, "must refuse to overwrite the input"
