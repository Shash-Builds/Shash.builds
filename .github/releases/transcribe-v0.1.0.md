<!-- Release notes for tag transcribe-v0.1.0. Push the tag and the release workflow attaches transcribe-skill.zip. -->

## Transcribe 0.1.0

**What it does:** Audio or video to transcript, SRT and VTT captions, and word timestamps with local Whisper. English, Hindi, Hinglish. Free, offline, no API key.

**Install:** download `transcribe-skill.zip` below and follow the 3 steps in [the README](../../tree/main/tools/toolbox/transcribe), or run the [toolbox installer](../../tree/main/tools/toolbox#install-everything).

### New
- Transcript (.txt), SRT and VTT captions, engine segments (.json) and a flat word list (.words.json)
- Models: small (default) or medium, plus base and large-v3
- English, Hindi, and Hinglish in Roman letters (`--hinglish`)
- Runs the shash.builds Transcriber engine; the zip bundles it

### Tested
- Linux (Python 3.13, ffmpeg 6.1). Windows commands are in the README and not tested on Windows yet.

---

Free and open source by shash.builds. Need a one-page website for your service business?
$400 flat, live in 7 days: https://github.com/Shash-Builds/shash.builds#hire-me
