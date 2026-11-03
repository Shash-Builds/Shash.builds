Turn any voice note, podcast, call or video into text and captions without uploading it anywhere.

This skill runs Whisper on your own computer through faster-whisper. Point it at an mp3, wav, m4a, mp4 or mov and you get four files: a plain transcript, SRT captions, WebVTT captions, and a JSON file with every word and its start and end time.

What it's good for:
- Captions for reels, shorts and YouTube videos, cut into short lines that read well on a phone
- Word timestamps for editing tools, silence cutting and burned-in word-by-word captions
- English, Hindi, and Hinglish written in Roman letters (one flag)
- Spelling names right: pass the names you expect and Whisper uses them

How it works:
- Model choice: small (fast, about 470 MB, downloaded once) or medium (more accurate, about 1.5 GB)
- Uses your GPU when one is set up, otherwise the CPU
- Works offline once the model is downloaded, or point it at a model folder you already have

Requirements: Python 3.9 or newer. ffmpeg is recommended (it reads every format) but optional.

Free and MIT licensed. Part of the shash.builds Toolbox, the small tools Shashwat Jain uses every day to make content.
