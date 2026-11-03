#!/usr/bin/env bash
# shash.builds Toolbox installer for macOS and Linux.
#   bash install.sh              every tool
#   bash install.sh transcribe   only the tools you name
# Installs ffmpeg (Homebrew on macOS, apt or dnf on Linux), then a Python virtual
# environment in tools/toolbox/.venv with each tool's requirements.txt.
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Installing ffmpeg..."
  if [[ "$(uname)" == "Darwin" ]]; then
    command -v brew >/dev/null || { echo "Install Homebrew first: https://brew.sh"; exit 1; }
    brew install ffmpeg
  elif command -v apt-get >/dev/null; then sudo apt-get update && sudo apt-get install -y ffmpeg
  elif command -v dnf >/dev/null; then sudo dnf install -y ffmpeg
  else echo "Install ffmpeg with your package manager, then run this again."; exit 1
  fi
fi

PY=$(command -v python3 || command -v python || true)
[[ -n "$PY" ]] || { echo "Install Python 3.9 or newer first: https://www.python.org/downloads/"; exit 1; }
"$PY" -c 'import sys; sys.exit(sys.version_info < (3, 9))' || { echo "Python 3.9 or newer is needed."; exit 1; }

[[ -d .venv ]] || "$PY" -m venv .venv
.venv/bin/python -m pip install --quiet --upgrade pip

tools=("$@")
if [[ ${#tools[@]} -eq 0 ]]; then
  for f in */requirements.txt; do tools+=("${f%%/*}"); done
fi
for t in "${tools[@]}"; do
  [[ -f "$t/requirements.txt" ]] || { echo "No tool called $t"; exit 1; }
  echo "Installing $t..."
  .venv/bin/python -m pip install --quiet -r "$t/requirements.txt"
done

echo
echo "Done. Start each session with:  source tools/toolbox/.venv/bin/activate"
echo "Then try:                        python tools/toolbox/transcribe/transcribe.py your-file.mp4"
