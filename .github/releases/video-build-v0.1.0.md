<!-- Release notes for tag video-build-v0.1.0. Push the tag and the release workflow attaches video-build-skill.zip. -->

## Video Build 0.1.0

**What it does:** A script file, voice and face clip to a finished 1080x1920 reel: shots on a timeline, word-by-word brand captions, music bed, -14 LUFS. Free and local.

**Install:** download `video-build-skill.zip` below and follow the 3 steps in [the README](../../tree/main/tools/toolbox/video-build), or run the [toolbox installer](../../tree/main/tools/toolbox#install-everything).

### New
- Reads the daily `video.md`: frontmatter, Shots table, Captions
- Shots: face, screen (image with a slow push-in, or video) and title cards
- Word-by-word brand captions with the spoken word in orange, plus on-screen text per shot
- 1080x1920, 30 fps, -14 LUFS, optional music bed with a credits file, optional end stinger

### Tested
- Linux (Python 3.13, ffmpeg 6.1). Windows commands are in the README and not tested on Windows yet.

---

Free and open source by shash.builds.
