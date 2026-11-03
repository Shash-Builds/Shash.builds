# Portfolio: concept sites by shash.builds

Sample one-page websites for made-up US service businesses, built the way a paid $400 site is built. Every business, phone number (555 numbers) and line of copy is sample content, and every page says so. No fake reviews or ratings: each page has an empty "Reviews go here" panel instead.

| Sample | Trade | Place | Style |
| --- | --- | --- | --- |
| [Caliche Ridge Roofing](roofer-tx/) | Roofing | San Antonio, TX | S-01 Swiss grid |
| [Saltbreeze Home Cleaning](cleaner-fl/) | House cleaning | Tampa, FL | S-05 Glass |
| [Coolwash Air Co.](hvac-az/) | AC and heating | Mesa, AZ | S-02 Night glow |
| [Red Clay & Fern Landscapes](landscaper-ga/) | Landscaping | Athens, GA | S-03 Organic |
| [Bluejay Plumbing Co.](plumber-oh/) | Plumbing | Dayton, OH | S-04 Playful blocks |
| [Lantern Row Barbershop](barber-ca/) | Barbershop | Long Beach, CA | S-08 Luxe |

More samples are on the way (dentist, auto repair). Each folder's `README.md` is its case card.

## How they're built

- `site.json` in each folder holds all the copy, photos and the style to use.
- `build.py` turns it into one self-contained `index.html` (CSS inline, photos as WebP next to it).
- `styles/base.css` is the shared layout, built on the [Mock Builder](../skills/mock-builder) skill's rules: call button in the first screen, sticky call bar on phones, a demo form that sends nothing, an empty reviews panel.
- `styles/s1.css` to `s8.css` are the 8 lookbook styles (Swiss grid, Night glow, Organic, Playful blocks, Glass, Editorial, Brutal, Luxe).
- `shots.cjs` makes the screenshots (1600x1200, 1080x1350, 1280x720, phone) and a scroll video.

```bash
python3 portfolio/build.py            # every sample
node portfolio/shots.cjs roofer-tx    # screenshots and scroll video (Playwright + ffmpeg)
```

Photos are CC0 (StockSnap, rawpixel, found through Openverse), credited on each page, with no people in them.
