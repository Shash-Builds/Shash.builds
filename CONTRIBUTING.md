# Contributing to shash.builds

Thanks for being here. This repo is one person building in public, so small, clear
contributions get merged fastest.

## Ways to help

- **Report a bug.** [Open a bug report](https://github.com/ShashwatBuilds/shash.builds/issues/new?template=bug.yml). Say which skill or tool, what you did, what you expected and what happened.
- **Ask for a skill or tool.** [Open an idea](https://github.com/ShashwatBuilds/shash.builds/issues/new?template=idea.yml). Best ideas solve one real job for a small service business or a web designer.
- **Fix something.** Typos, broken links and clearer install steps are always welcome.
- **Share a result.** Used a skill on a real project? Tell me in an issue. It helps me decide what to build next.

## Pull requests

1. Fork the repo and make a branch: `git checkout -b fix/short-name`.
2. Keep each PR to one change.
3. Run the repo check before you push:

   ```bash
   python3 scripts/check.py
   ```

4. Open the PR and fill in the template.

## House rules for every file

- **Same layout everywhere.** A new skill or tool gets its own folder with a README that follows [`templates/ITEM-README.md`](templates/ITEM-README.md), a header from `python3 media/build.py header`, and a row in `catalog.json`.
- **Write like a person.** Short sentences, US English, no em dashes, no filler.
- **True claims only.** No made-up users, reviews, numbers or logos. Example numbers say "example".
- **Alt text on every image.**
- **No secrets, no personal data.** No API keys, tokens, phone numbers, private emails, client data or photos of people.
- **No big binaries.** Video and audio go in GitHub Releases, not in git.
- **Licenses.** Code is MIT. Content in `content/` and `media/` is CC BY 4.0. Anything you add from elsewhere must allow commercial use and redistribution, and gets credited.

By contributing, you agree your work is released under the same licenses.

## Questions

Open a [discussion-style issue](https://github.com/ShashwatBuilds/shash.builds/issues/new?template=idea.yml) or message Shashwat on [LinkedIn](https://www.linkedin.com/in/shashbuilds).
