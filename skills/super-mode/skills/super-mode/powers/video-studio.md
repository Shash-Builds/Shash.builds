# Power: Video Studio

For any video: reels, explainers, ads, screen walkthroughs, talking heads, animations, captions, voice, music.

## Builds on
- The **master** skill's video workflow (`skills/master/skills/master/workflows/video.md`): the 8-stage loop
  (brief, taste, build, harsh review, fix list, up to 3 regenerations), the HTML frame renderer, the sound kit.
- **motion-design-taste** (`skills/motion-design-taste/skills/motion-design-taste/motion-design-taste.md`),
  **audio-review**, **transcriber**, **clipper**, **ai-visuals**, **humanizer** for every word on screen.

## Watch the reference first
When the user sends a reference video, watch it, not just its caption: turn it into frame sheets (one frame
a second, tiled), read the on-screen text, transcribe the audio, and note the cuts, captions and sound.
Save a labelled row in the project's references index.

## Talk first
Say the plan: format and length, the look (two or three named references), the voice, music and sound,
and what you will show before the full render (a 5 to 10 second sample or 3 still frames). Wait for "go".

## Voice: make a phone sound like a studio
1. Clean with DeepFilterNet 3 if installed (`python3 scripts/setup.py --yes --voice` in the shash.builds repo).
2. Polish word by word: high-pass, breaths and mouth noise between words turned down (not cut, so it stays
   human), mud cut and a little presence, de-ess only when "s" spikes, gentle compression, quiet words lifted.
3. Loudness: -14 LUFS for reels and Shorts, -16 for Loom and long talks, true peak -1.5 dB.
4. The voice always sits above music and effects. Check by ear and by numbers before you hand it back.

## Cut what wastes the viewer's time
- **Fillers:** normal transcription silently drops "um" and "uh". Run a second, word-for-word pass (give
  Whisper a prompt full of fillers, for example "Umm, so, uh, I was like, hmm") and also flag gaps between
  words that still carry voice energy (held "uhh"). Cut each with a short crossfade.
- **Repeated words** ("very very"): keep the second.
- **Silence:** where nobody speaks, make it silent, not room noise.
- **Screen recordings:** a static wait (loading, typing) keeps 1.5 s before and 1.5 s after the change and
  never holds more than 3 s; a busy screen with no speech is sped up instead of cut.

## Look
- Smooth 2D with depth, many small connected elements, each with its own entrance. No 3D unless asked, no
  fake or stock-AI look, no serif headlines (a modern sans pair, for example Bricolage Grotesque and Geist).
- **Never three repeating looks.** Rotate edit treatments on a talking head (zoom, black and white, rim light,
  side swap, flash, picture in picture, centre) and change something every 2 to 4 seconds.
- Cut-out of the speaker (MediaPipe selfie segmentation), filled from the shoulders down so the chest is
  never lost; words can sit behind the head.
- Montages over long full-screen face shots. Chapter cards, a thin progress bar and captions placed clear
  of the platform's buttons for anything over a minute.

## Motion rules (from open-source motion studies, credited below)
- Moves land with an ease-out and leave with a shorter ease-in. Arrivals decelerate from oversize (logos
  from about 3.5x) instead of growing from zero.
- In the best moments almost every frame moves; flag any still run longer than about 0.3 s that is not a
  deliberate hold.
- Every cut hands something over: speed, scale direction, shape or position. The incoming move starts near
  the outgoing speed and settles. Effects land on the exact frame of their motion.
- Cuts every 0.3 to 2.3 s in fast films; the end card holds 0.6 to 1.4 s, not longer.

## Free voice and 3D (optional tools)
- **Voiceover without a voice actor:** Chatterbox (MIT, github.com/resemble-ai/chatterbox) reads a script
  aloud for free on the user's own machine. Clone a voice only with that person's clear permission (their
  own voice is fine), and say in the delivery note that the voice is generated.
- **Captions:** faster-whisper, which the transcriber skill already uses, with word-level timing.
- **Real 3D:** Blender MCP (MIT, github.com/ahujasid/mcp-for-blender) lets Claude drive Blender for 3D shots.
  Use it only when the user asks for 3D; the default look stays 2D with depth.

## Sound
- One accent every 1 to 2 seconds on reels (whoosh on transitions, pop or tick on small elements, one
  impact for the big moment), synced to cuts, about 10 dB under the voice.
- Music fitted to the exact length by repeating whole sections at clean joins, never cut off mid-phrase;
  cut on the beat where you can (librosa beat detection).
- Only licensed audio: the master skill's sound library (with its credit lines), CC0 sounds, or the user's
  own files. Copyrighted songs go only into private videos the user owns the right to show.

## Deliver
- Inspect before you show it: motion-design-taste's `inspect_video.py`, audio-review's `analyze.py`.
- Full quality only. If a file is too big for the channel, split it into parts under the limit and give a
  way to join them; never shrink quality without asking.
- Say what you made in 3 lines and which checks it passed.

## Done when
- The user approved the plan and the sample.
- Voice clean and above the music; no fillers, dead air or waits over 3 s.
- Taste score 85+ or the user accepted it; no repeating looks; captions readable and clear of buttons.
- Licences and credits listed for every outside sound, font and image.

## Credits
Motion timing ideas from motionmaxxing (Apache-2.0, github.com/Tejashmakwana/motionmaxxing), cinetic (MIT,
github.com/Leonxlnx/cinetic) and huashu-art-motion (MIT, github.com/alchaincyf/huashu-art-motion). Ideas
only; no text or code copied.
