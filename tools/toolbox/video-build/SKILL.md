---
name: video-build
description: Build a finished 1080x1920 vertical video from a day's video.md, a voice track, a face clip and screenshots, on the user's computer: shots cut to a timeline, word-by-word brand captions, on-screen text, optional music bed, -14 LUFS. Use for "build today's video", "render the reel", "make the daily video".
---

The script sits next to this SKILL.md (in Claude Code: `${CLAUDE_SKILL_DIR}/video_build.py`).
It needs ffmpeg, Pillow and, for captions, the transcribe tool (its folder sits beside this one
in the toolbox) or a NAME.words.json.

1. Read the user's video.md. If there isn't one, write it with them in the format shown at
   the top of video_build.py: frontmatter (voice, face, music), a Shots table
   (`at | shot | on-screen text`, shots are `face`, `screen: FILE` or `title`), Captions
   (`burn: yes`). Paths are relative to video.md.
2. Preview: `python video_build.py video.md --dry-run` prints every shot with its start and
   end. Check the shots cover what the script says and nothing runs past the voice.
3. Build: `python video_build.py video.md -o day-01.mp4`. Add `--stinger FILE` for the closing
   stinger, `--words voice.words.json` if the voice is already transcribed, `--model medium`
   for Hindi.
4. Check the result before handing it over: look at a frame from each shot and read the
   captions for misheard words. Fix a misheard word by editing the words.json and passing it
   with `--words`.
5. If music has a credit (`music: file.mp3 | credit`), give the user the line in
   OUTPUT.credits.txt for the post caption.

Only use music the user has the rights to (royalty-free with its license, or their own).
