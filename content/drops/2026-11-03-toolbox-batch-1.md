# Drop: the Toolbox, batch 1 (2026-11-03)

Five free command-line tools that make the daily video, each also a Claude skill:
transcribe, cut-silence, video-build, repurpose, photo-kit. MIT licensed, run locally, no API keys.

Repo: https://github.com/ShashwatBuilds/shash.builds/tree/main/tools/toolbox

Install (macOS or Linux):

```
git clone https://github.com/ShashwatBuilds/shash.builds
bash shash.builds/tools/toolbox/install.sh
```

Windows: `powershell -ExecutionPolicy Bypass -File tools\toolbox\install.ps1` (only post this line once Shashwat has run it on Windows).

Facts every post must keep true:

- Free and MIT. No signup, no paid tier, no paid API anywhere in the path.
- Everything runs on your computer. Only models are downloaded (Whisper small about 470 MB, medium about 1.5 GB; rembg about 170 MB), once.
- Tested on Linux only so far. Don't say "works on Windows" until the Windows checklist is done.
- repurpose doesn't call a model by itself: it writes a prompt for Claude or any chat model, or uses a local Ollama model if you have one, then checks the answer.
- photo-kit always strips EXIF and GPS. There's no option to keep them.
- The Agensi listings are not live. Don't link agensi.io until Shashwat approves each listing.

Times and rules come from `research/communities.md` (checked 2026-11-03); most rules there are unverified, so open each sidebar before posting. LinkedIn and X times are guesses and marked that way.

---

## 1. r/ClaudeAI (Built with Claude showcase megathread comment)

Place rules (map row 1): showcase posts go through the megathread.
Suggested: a weekday, late morning ET.

```
I made the tools I use to ship a vertical video every day into Claude skills. Free, MIT, all local.

transcribe: audio or video to transcript, SRT/VTT and word timestamps (faster-whisper, small or medium, English and Hindi)
cut-silence: cuts pauses and "umm"s with ffmpeg, keeps a 0.15 s pad
video-build: a video.md shot list + voice + face clip to a 1080x1920 reel with word-by-word captions, -14 LUFS
repurpose: transcript to LinkedIn, Instagram, X thread and YouTube chapters, then a script checks every limit
photo-kit: every platform size from one photo, EXIF and GPS always stripped

No API keys. Tested on Linux so far.
https://github.com/ShashwatBuilds/shash.builds/tree/main/tools/toolbox
```

## 2. r/SideProject (map row 11, launch posts welcome)

Suggested: a weekday morning ET.

```
Title: I open-sourced the 5 scripts that make my daily build-in-public video

Every day I record a 2-minute video. These five tools turn the raw recording into the reel and the posts:

1. transcribe: local Whisper, captions with word timings
2. cut-silence: removes pauses and umms, keeps 0.15 s around speech
3. video-build: a markdown shot list to a finished 1080x1920 video with burned-in captions
4. repurpose: one transcript to four posts, checked against each platform's limits
5. photo-kit: one photo to 8 platform sizes, location data stripped

All free, MIT, no paid APIs, everything runs on your machine. Each one is also a Claude skill.
Repo: https://github.com/ShashwatBuilds/shash.builds/tree/main/tools/toolbox

What would you add to the kit?
```

## 3. LinkedIn (time is a guess: Tuesday to Thursday, 8 to 10 am in your audience's time zone)

```
5 scripts make my daily video.

I record 2 minutes. Then:
transcribe writes the captions,
cut-silence removes the pauses and umms,
video-build turns a shot list into a finished vertical video,
repurpose writes this post and three more from the transcript,
photo-kit makes every image size and strips the location data.

All five are free and open source now, and each one is also a Claude skill. They run on your computer with no API keys.

Link in the first comment.

Which step of your content takes the longest?
```

First comment: `https://github.com/ShashwatBuilds/shash.builds/tree/main/tools/toolbox`

## 4. X (time is a guess: weekday, 9 am to noon ET)

```
1/ I open-sourced the 5 tools that make my daily video. Free, MIT, all local, no API keys.

2/ transcribe: Whisper on your machine. Captions, word timings, English and Hindi.

3/ cut-silence: pauses and umms out, 0.15 s kept around every word.

4/ video-build: a markdown shot list + voice + face clip to a 1080x1920 reel with brand captions.

5/ repurpose writes the posts, photo-kit makes every image size and strips GPS.
https://github.com/ShashwatBuilds/shash.builds/tree/main/tools/toolbox
```

## 5. Agensi (map row 17): not yet

Five listings are prepared in `tools/toolbox/<tool>/agensi/` (title, summary, description, tags, cover, price free). Nothing goes live until Shashwat approves each one.
