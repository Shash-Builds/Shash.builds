---
name: cut-silence
description: Cut silences and "umm" or "uh" fillers out of a face recording or voice-over on the user's computer with ffmpeg, keeping a 0.15 second pad so speech never sounds clipped. Use for "cut the silences", "remove the umms", "tighten this recording", jump cuts.
---

The script sits next to this SKILL.md (in Claude Code: `${CLAUDE_SKILL_DIR}/cut_silence.py`).
It needs ffmpeg and ffprobe on PATH and nothing else.

1. To cut fillers too, transcribe first (the transcribe skill writes NAME.words.json).
2. Preview: `python cut_silence.py INPUT --words NAME.words.json --dry-run` prints the
   old and new length and every cut. Tell the user the numbers.
3. Cut: `python cut_silence.py INPUT --words NAME.words.json -o OUTPUT`. Leave out
   `--words` to cut silences only. Defaults: `--pad 0.15`, `--min-silence 0.4`,
   `--threshold -35` (use -30 in a noisy room, -45 if quiet speech gets cut).
4. It writes OUTPUT and OUTPUT.cuts.json (kept and removed ranges). Captions made before
   the cut no longer line up: transcribe the cut file again for captions.

Never overwrite the user's original; the script refuses to.
