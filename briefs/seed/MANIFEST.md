# Seed export manifest

Exported 2026-11-03 by branch chat 2 for the shash.builds factory. Nothing here is deployed. The factory moves each item to its home in the repo, and the site ships only after Shashwat approves.

## Sources

| Short name | Repo | Branch | Commit |
| --- | --- | --- | --- |
| `private` | the private working repo | `claude/closer-portfolio-sample-designs-0cmtin` | `3a7a104` |
| `media` | the old media repo (public) | default | `904b6a3` |

Nothing was copied from `media`. It holds other projects (finance videos, an apparel store, app courses), not the web design work, and its one trailer folder is for a different product.

## How every file was checked

1. Every image was opened and looked at. Every video was cut into a contact sheet of frames and looked at. None of the copied files shows a person.
2. Every text file was searched for emails, phone numbers, WhatsApp links, account or seller IDs, keys and tokens, and old brand names. All were removed or never present.
3. PNG and WebM metadata was read: only encoder tags, no names, paths or locations.
4. `python3 scripts/check.py` passes, and a case-insensitive search for the old brand names returns 0 hits.

## Files copied

### `site/`: the portfolio website, built output only

From `private:closer-portfolio/`. Ready to deploy after approval.

| File | Changes made | Why it's safe |
| --- | --- | --- |
| `index.html` | Removed the embedded photo of Shashwat (hero) and put Tab (`tab.svg`) in its place. Removed the personal email (4 places), the WhatsApp number and link, and the `og.jpg` image tags (that image is a photo of Shashwat). LinkedIn now points to `linkedin.com/in/shashbuilds`, like the rest of the repo. The booking button opens LinkedIn until a booking link exists. Title and footer say shash.builds. | The 4 remaining embedded images are screenshots of fictional sample sites (gym, dentist, realtor, salon) with no people. Price, hours and process are Shashwat's public offer. |
| `lookbook.html` (8 styles, 12 kinds of business) | Removed the email and WhatsApp number from the script. The "Book a call with this style" button opens LinkedIn. Removed the `og.jpg` tag. Title says shash.builds. | All businesses, names and quotes are fictional sample content shown inside a "Sample design" frame. Visitor photos stay in the browser (the page says so and never uploads them). |
| `skills.html` | Removed the `og.jpg` tag. Title says shash.builds. | Public page for the free skill. Credits the third-party Hallmark skill with a link. |
| `robots.txt` | None | Allows all crawlers. |
| `sitemap.xml` | None | Three public URLs. |
| `llms.txt` | Removed the email and WhatsApp number. Added LinkedIn and GitHub. Title says shash.builds. | Public summary of the offer. |
| `tab.svg` | New copy of `media/tab-static.svg` from this repo | Our own mascot, replaces the photo. |
| `skills/booked-one-pager/SKILL.md` | None | The site's skills page links to it at this path. Same file as `skills/booked-one-pager/SKILL.md` below. |

### `skills/booked-one-pager/`: the free skill

| File | From | Why it's safe |
| --- | --- | --- |
| `SKILL.md` | `private:closer-portfolio/skills/booked-one-pager/SKILL.md` | A public, free how-to with no personal or client data. Needs the repo's plugin layout (README, header, plugin.json, catalog row) when the factory adds it to `skills/`. |

### `mascot/`: Tab

| File | From | Why it's safe |
| --- | --- | --- |
| `sheet.html`, `tab-sample-sheet.png` | `private:closer-portfolio/mascot/` | Character sheet. Drawings only. |
| `tab.js` | `private:content/built-in-bed/src/tab.js` | The code that draws Tab as SVG. No notes, no data. |
| `stills/tab-*.png` (8 files) | `private:content/built-in-bed/mascot/` | Expressions: neutral, sceptic, thinking, excited, booked, mouth A, O, E. |
| `motion/tab-*.webm` (4 files) | `private:content/built-in-bed/mascot/` | Idle, talk, think and booked loops with a transparent background. |

### `trailer/`: trailer scenes, HTML only

| File | From | Changes made |
| --- | --- | --- |
| `scene.html`, `scene-v2.html`, `scene-long.html` | `private:closer-portfolio/trailer/` | The photo of Shashwat (`caps/me.webp`) is now `caps/tab.png`. Header comments no longer name the song, the music file or the old repo. "The founder rises" comments now say Tab. |

The screenshots in `caps/`, the fonts and the capture scripts were not copied, so the scenes need fresh captures before they render.

### `built-in-bed/`: series graphics with no people

From `private:content/built-in-bed/`.

| File | What |
| --- | --- |
| `brand/logo-cream.png`, `brand/logo-ink.png` | Series wordmark with Tab |
| `brand/title-sting.webm` | 2.4 s opener |
| `overlays/sticker-*.png` (7 files) | $400, 7 DAYS, FREE, BOOKED, IN BED, AI DID THIS, 0 CODE |
| `overlays/lower-third.webm` | Name strip with Shashwat's public name, no photo |
| `overlays/prompt-1-build.webm`, `prompt-2-bolder.webm`, `prompt-3-booking.webm` | "YOU TYPE" prompt cards |
| `overlays/cta-comment-site.webm`, `cta-dm-site.webm` | End cards with Tab |
| `overlays/wipe-orange.webm` | Transition |

## Not copied, and why

| Item | Reason |
| --- | --- |
| `closer-portfolio/me/`, `og.jpg`, `trailer/caps/me.webp`, the hero photo inside `index.html` | Photos of a person |
| `closer-portfolio/src/`, `content/built-in-bed/src/` (except `tab.js`) | Build sources with working notes |
| `PLAN.md`, `NEXT.md`, `HANDOVER.md`, `allowed-domains.*`, the series scripts and recording guide | Plans and internal notes |
| `music/`, every file "WITH-SONG" | Songs not licensed for redistribution |
| `broll/*.mp4` | The portfolio scroll shows the photo of Shashwat; all three are videos, and videos go in Releases |
| `tracking/*.mp4` | No people and labelled example numbers, so safe, but `.mp4` files are kept out of git. Attach them to a Release if wanted |
| `sfx/*.wav` | Our own synthesised sounds, but the repo keeps audio out of git. Attach to a Release if wanted |
| `skills/booked-one-pager.zip` | Zips are built by the release workflow, not committed |
| `outputs/`, `trailers/`, other renders | Other projects or renders with songs |
| `img/sample-*.webp` | Not used by the built pages (the screenshots are embedded in `index.html`) |
| Any CLAUDE.md, memory sheet, account or seller IDs, client data | Never exported |

## Open items for the factory and Shashwat

1. **LinkedIn URL.** Resolved 2026-11-04: the profile isn't live yet, so every LinkedIn link now opens an email to shash.builds@gmail.com instead. Old note: The site now links to `linkedin.com/in/shashbuilds`, matching this repo. If that URL isn't live yet, change it back to the current profile URL before deploy.
2. **Share image.** `og.jpg` was a photo, so the pages have no `og:image` now. Make one from the media kit (for example `media/social-preview.png`) before deploy.
3. **Site address.** Canonical URLs and the sitemap still use `shashwat-websites.netlify.app`. Update them if the shash.builds site gets its own address.
4. **Booking link.** Paste it into `CALENDLY` in `index.html` and `lookbook.html` when it exists.
5. **Skill zip.** `skills.html` links to `skills/booked-one-pager.zip`. Build it at deploy time or point the link at the GitHub Release.
