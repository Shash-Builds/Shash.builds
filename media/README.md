# Media kit

Everything visual for shash.builds. Text in every SVG is drawn as outlines, so files look
the same everywhere with no font loading. Rebuild the whole kit with one command:

```bash
pip install fonttools uharfbuzz
python3 media/build.py
```

## Files

| File | Size | Use |
| --- | --- | --- |
| `banner.svg` | 1280 x 440 | Top of the main README. Tab blinks and bobs (stops for reduced motion). |
| `social-preview.png` / `.svg` | 1280 x 640 | GitHub social preview and link cards |
| `profile-header.svg` | 1280 x 360 | GitHub profile README |
| `tab.svg`, `tab-static.svg` | 200 x 200 | Tab the mascot, animated and still |
| `header-example.svg` | 1280 x 300 | Shows the per-item header. Make one with `python3 media/build.py header "Name" --kind skill --line "One line" --out path/header.svg` |
| `icons/*.svg` | 48 x 48 | skill, tool, template, video, content, research, hire, log |

## Brand

| Token | Value | Use |
| --- | --- | --- |
| Signal orange | `#e8572c` | The dot in the wordmark, accents, one per view |
| Ink | `#15120f` | Backgrounds, outlines |
| Cream | `#f6efe3` | Text on ink, Tab's body |
| Display font | Bricolage Grotesque 800 | Wordmark and titles |
| Body font | Onest 400 and 600 | Everything else |

**Name:** always "shash.builds", lowercase, with the dot in orange. Where a dot isn't allowed, "shashbuilds".

**Tab:** a browser tab (websites), an AI spark (Claude) and calendar rings (ships on a schedule). Keep the spark orange and the face simple.

## Credits

- [Bricolage Grotesque](https://github.com/ateliertriay/bricolage) by Mathieu Triay, SIL Open Font License 1.1.
- [Onest](https://github.com/simpals/onest) by Dmitri Voloshin and Andrey Kudryavtsev, SIL Open Font License 1.1.
- Rendered with [fontTools](https://github.com/fonttools/fonttools) (MIT) and [uharfbuzz](https://github.com/harfbuzz/uharfbuzz) (Apache 2.0).

Artwork is CC BY 4.0. `build.py` is MIT.
