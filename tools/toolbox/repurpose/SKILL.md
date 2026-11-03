---
name: repurpose
description: Turn one video transcript into a LinkedIn post, an Instagram caption with 3 hashtags, an X thread and a YouTube title, description and chapters, in a human tone with no em dashes, then check every limit with a script. Use for "repurpose this video", "write the posts for today's video", "YouTube chapters".
---

The script sits next to this SKILL.md (in Claude Code: `${CLAUDE_SKILL_DIR}/repurpose.py`).
No packages needed.

1. Get a transcript: the .srt or .json from the transcribe tool is best (it has timings for
   chapters); a .txt works too.
2. Run `python repurpose.py prompt TRANSCRIPT --topic "one line on the video"`. It writes
   NAME.repurpose-prompt.md with the rules, the output format and the transcript with
   [mm:ss] marks.
3. You are the model: read that prompt file and write the answer exactly in its format to
   NAME.repurpose.md. Use only facts in the transcript. If the humanizer skill is
   installed, run each piece through it on its channel.
4. Run `python repurpose.py check NAME.repurpose.md`. Fix every line it prints and check
   again until it says ok.
5. Show the user the four pieces. Never post them anywhere; the user posts.

`example.repurpose.md` next to this file shows a passing answer.
