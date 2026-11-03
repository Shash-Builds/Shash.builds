---
name: transcribe
description: Transcribe audio or video on the user's own computer with local Whisper (faster-whisper): plain transcript, SRT and VTT captions, and word timestamps. English, Hindi and Hinglish. No API key, nothing uploaded. Use for "transcribe this", "make captions", "subtitles for this video".
---

The script sits next to this SKILL.md (in Claude Code: `${CLAUDE_SKILL_DIR}/transcribe.py`).

1. Check the file exists. If `python -c "import faster_whisper"` fails, install once:
   `python -m pip install -r requirements.txt` (the file next to this SKILL.md).
2. Pick the model: `small` by default; `medium` when the user wants better accuracy, the
   audio is noisy, or it's Hindi. Pick the language: `auto`, `en`, `hi`, or `--hinglish`
   when the user wants Hindi written in Roman letters.
3. Run `python transcribe.py FILE --model small --out-dir <folder>`. Add
   `--prompt "brand names, people's names"` when the user mentions names that must be
   spelled right.
4. It writes NAME.txt, NAME.srt, NAME.vtt and NAME.words.json and prints their paths.
   Show the user the transcript, say how many words were unsure (printed on stderr), and
   offer the next step: cut-silence, video-build or repurpose.

Never send the audio anywhere. The first run downloads the model once (small about 470 MB,
medium about 1.5 GB); tell the user before starting a medium run.
