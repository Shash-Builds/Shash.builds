# Power: Desktop

For Claude on the user's own computer and phone: setting a machine up, driving desktop apps, running AI
locally and linking a cloud chat to the computer. Product names and menus change: check the current
Claude Code docs before giving steps.

## Builds on
The **helper** power for step-by-step fixes with a non-technical user, the **operator** power for long
set-ups, `scripts/setup.py` in the shash.builds repo to install every tool the skills use.

## Where Claude runs
- **In the cloud:** a fresh machine per session. Good for code, research, renders. It cannot see the
  user's files, apps or phone unless they connect them.
- **On the computer:** Claude Code in the terminal or the desktop app works on local files and apps.
- **Cloud chat, local computer:** Remote Control lets a cloud session use a folder the user shares from
  their computer. Computer use (in the Claude desktop app) lets Claude see the screen and click and type,
  with the user's approval per app. Claude in Chrome acts in the user's own browser.
Pick the smallest one that does the job, and say which one and why.

## Setting up a machine
1. Back up first. Before wiping or installing an operating system, copy the user's files somewhere safe
   and check the copy opens.
2. Windows apps in one go: Ninite (type ninite.com exactly; look-alike sites carry malware).
3. Linux on the user's own laptop: a mainstream release (for example Ubuntu LTS) from its official site,
   written to a USB stick, tried live before installing.
4. Then the toolkit: `python3 scripts/setup.py` (check), `--yes` (install), `--yes --voice` (voice cleaning).
5. Write what was installed and how to undo it in a short setup note in the user's project.

## Driving desktop apps
- **CLI-Anything** (Apache-2.0, github.com/HKUDS/CLI-Anything): a command-line version of apps like OBS,
  Blender, GIMP, Audacity and LibreOffice, so Claude can use them by text.
- **Blender MCP** (MIT, github.com/ahujasid/mcp-for-blender): Claude drives Blender for 3D shots.
- Prefer an app's own command line or files over clicking through its screen; it is faster and repeatable.

## Local AI (free, private, needs the hardware)
- Captions and transcripts: faster-whisper (runs on a normal laptop).
- Voiceover: Chatterbox (MIT, github.com/resemble-ai/chatterbox); clone a voice only with that person's
  permission.
- Local chat models: Ollama, for second opinions without a cloud key.
- AI video: FreeVideo (Apache-2.0, github.com/FlashML-org/FreeVideo) needs a graphics card with 8 GB of
  video memory and 16 GB of RAM. Check the machine before suggesting it.

## Android phone
- scrcpy (Apache-2.0, github.com/Genymobile/scrcpy) shows and controls the phone from the computer over USB.
- adb (Android platform-tools from developer.android.com) installs apps and copies files. Turn on USB
  debugging only on the user's own phone, and turn it off when done.

## Never
Get around a lock, account or security control on a device that is not the user's. Install anything
without saying what it is and getting a yes. Ask for or store passwords. Automate fake activity on
social apps (bot likes, phone farms).

## Done when
The machine or app does what the user wanted, every install was approved and is written down with how to
undo it, and the user's files are safe.
