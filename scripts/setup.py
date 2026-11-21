"""Set up everything in shash.builds on this computer: the Claude Code plugins and every tool the skills use.

Usage:
  python3 scripts/setup.py            check only: what is installed and what is missing (changes nothing)
  python3 scripts/setup.py --yes      install the missing Python packages
  python3 scripts/setup.py --yes --voice   also install DeepFilterNet (studio voice cleaning, about 2 GB) in its own folder

It never uses sudo and never installs system programs itself: for ffmpeg, Node.js and the browser it prints the
one command for this system. The plugins are installed inside Claude Code with the /plugin lines it prints."""
import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = {  # import name: pip name (what the skills' scripts use)
    "numpy": "numpy", "PIL": "pillow", "faster_whisper": "faster-whisper", "soundfile": "soundfile",
    "pyloudnorm": "pyloudnorm", "pedalboard": "pedalboard", "yt_dlp": "yt-dlp", "anthropic": "anthropic",
    "librosa": "librosa",
}
VOICE_DIR = Path.home() / ".shashbuilds" / "voicefx"


def say(ok: bool, name: str, hint: str = "") -> None:
    print(f"  {'OK     ' if ok else 'MISSING'} {name}" + (f"  ->  {hint}" if hint and not ok else ""))


def system_hint(tool: str) -> str:
    osname = platform.system()
    if tool == "ffmpeg":
        return {"Darwin": "brew install ffmpeg", "Windows": "winget install ffmpeg"}.get(osname, "sudo apt-get install -y ffmpeg")
    if tool == "node":
        return {"Darwin": "brew install node", "Windows": "winget install OpenJS.NodeJS"}.get(osname, "sudo apt-get install -y nodejs npm")
    return ""


def has_module(name: str) -> bool:
    try:
        __import__(name)
        return True
    except Exception:
        return False


def plugins() -> list:
    try:
        return [p["name"] for p in json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))["plugins"]]
    except (OSError, ValueError, KeyError):
        return []


def main(argv: list) -> int:
    yes, voice = "--yes" in argv, "--voice" in argv
    unknown = [a for a in argv if a not in ("--yes", "--voice", "--check")]
    if unknown:
        print(f"Unknown option {unknown[0]}. Use --yes to install, --voice for DeepFilterNet, or nothing to check.")
        return 2
    print("1/4 Programs")
    for tool in ("ffmpeg", "node"):
        say(bool(shutil.which(tool)), tool, system_hint(tool))
    pw = bool(shutil.which("node")) and subprocess.run(
        ["node", "-e", "require('playwright')"], capture_output=True).returncode == 0
    say(pw, "playwright (browser for video renders)", "npm i -g playwright && npx playwright install chromium")

    print("2/4 Python packages")
    missing = [pip for mod, pip in PACKAGES.items() if not has_module(mod)]
    for mod, pip in PACKAGES.items():
        say(pip not in missing, pip, f"pip install {pip}")
    if missing and yes:
        print(f"  installing: {' '.join(missing)}")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", *missing])
        print("  done" if r.returncode == 0 else "  some packages failed; run the pip line above by hand to see why")

    print("3/4 Studio voice cleaning (DeepFilterNet, optional)")
    vpy = VOICE_DIR / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")
    say(vpy.exists(), f"DeepFilterNet in {VOICE_DIR}", "python3 scripts/setup.py --yes --voice")
    if voice and yes and not vpy.exists():
        print("  installing DeepFilterNet (large download)")
        steps = [[sys.executable, "-m", "venv", str(VOICE_DIR)], [str(vpy), "-m", "pip", "install", "-q", "torch",
                 "--index-url", "https://download.pytorch.org/whl/cpu"], [str(vpy), "-m", "pip", "install", "-q", "deepfilternet", "soundfile"]]
        for s in steps:
            if subprocess.run(s).returncode != 0:
                print("  stopped: that step failed. DeepFilterNet is optional; everything else still works.")
                break

    print("4/4 Claude Code plugins (paste these into Claude Code)")
    names = plugins()
    if not names:
        print("  could not read .claude-plugin/marketplace.json")
    else:
        print("  /plugin marketplace add Shash-Builds/shash.builds")
        for n in names:
            print(f"  /plugin install {n}@shashbuilds")
    if not yes:
        print("\nChecked only, nothing changed. Run with --yes to install the missing Python packages.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
