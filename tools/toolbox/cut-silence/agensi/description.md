Talking-head videos get tighter when the dead air goes. This skill does that pass for you, on your own computer.

It finds every pause longer than 0.4 seconds with ffmpeg's silence detector and cuts it, leaving 0.15 seconds of room around your words so nothing sounds chopped. Give it the word timings from the Transcribe skill and it also cuts "umm", "uh", "er" and "hmm", plus the gap around them.

What you get:
- A new video (or audio file) with the cuts made, picture and sound in sync
- A cuts file listing every part kept and removed, with times, so you can check it or line up edits
- A dry-run mode that shows the cuts before anything is written

You control:
- The pad around speech, the shortest pause to cut, and the silence level for noisy rooms
- Which filler words count

Requirements: ffmpeg. No Python packages. Your original file is never overwritten.

Free and MIT licensed. Part of the shash.builds Toolbox.
