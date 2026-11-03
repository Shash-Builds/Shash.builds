<!-- Release notes for tag cut-silence-v0.1.0. Push the tag and the release workflow attaches cut-silence-skill.zip. -->

## Cut Silence 0.1.0

**What it does:** Cuts silences and umm or uh fillers from a face recording or voice-over with ffmpeg, keeping a 0.15 s pad. Free, local, no API key.

**Install:** download `cut-silence-skill.zip` below and follow the 3 steps in [the README](../../tree/main/tools/toolbox/cut-silence), or run the [toolbox installer](../../tree/main/tools/toolbox#install-everything).

### New
- Cuts pauses over 0.4 s, keeping a 0.15 s pad around speech
- Cuts "umm", "uh" and other fillers using word timings from transcribe
- `--dry-run` preview and a `.cuts.json` report of every part kept and removed
- ffmpeg only, no Python packages

### Tested
- Linux (Python 3.13, ffmpeg 6.1). Windows commands are in the README and not tested on Windows yet.

---

Free and open source by shash.builds. Need a one-page website for your service business?
$400 flat, live in 7 days: https://github.com/ShashwatBuilds/shash.builds#hire-me
