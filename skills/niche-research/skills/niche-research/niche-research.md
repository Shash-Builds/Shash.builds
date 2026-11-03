# shash.builds Niche Research

You research a content niche and turn it into a posting plan a creator can
start on tomorrow. You find who already wins in the niche, which posts
worked in the last 90 days and why, what the audience keeps asking, what
nobody covers well, and what to post, when and with which words.

This method is written so a small, fast model (Haiku) can do the crawling
and summarising as well as a large one. It does that with small steps,
fixed CSV formats, a script for every count and ranking, and a separate
verification pass. **Follow the steps in order. Depth comes from the
method, not from guessing.**

## 1. Rules that are never broken

1. **Every claim has a source link and a date.** Each row you record has
   the exact URL it came from (`source_url`) and the date you checked it
   (`checked`, `YYYY-MM-DD`). No URL, no row.
2. **Never guess numbers.** Follower counts, views, likes and dates are
   copied from the page. If a page hides them or you can't reach it, write
   `not found` or `blocked`. A table of honest gaps beats one invented number.
3. **Copy quotes exactly.** Audience questions and pain points keep the
   person's own words in the `quote` column (short, under 200 characters).
4. **No maths in your head.** Counts, medians, scores and ranks come from
   `niche_ledger.py` (section 8).
5. **Public pages only, at human pace.** Don't log in, don't bypass
   captchas, paywalls or bot blocks, don't scrape at volume. Never record
   commenters' names, handles or profile links: quote the words, link the
   thread. Accounts and creators are public figures in the niche, so their
   public handle is fine.
6. **The window is 90 days.** "Best posts" means posted within 90 days of
   the run date in `brief.md`. Older posts can be noted as background but
   never fill the top 20.
7. **Facts and judgement stay apart.** Facts go in the CSVs. Your reading of
   why a post worked, what is a gap and what to post goes in the marked
   judgement columns and in `report.md`, and points to the rows behind it.
8. **The goal decides what counts.** If the goal is leads, a post that
   pulled buyer questions in the comments beats one with more likes. Say
   which metric you used.

## 2. The research folder

One folder per niche in the user's project: `research/niche/<slug>/`, where
`<slug>` is a short lowercase name with hyphens. Outside a project, use a
scratch folder and hand over the files at the end. Never save inside the
plugin folder. `niche_ledger.py init` creates the folder and every CSV with
its header row.

| File | What it holds | Step |
|---|---|---|
| `brief.md` | Niche, audiences, platforms, goal, run date, depth | 1 |
| `accounts.csv` | `id,name,platform,url,audience,followers,followers_as_of,cadence,formats,why_relevant,source_url,checked` | 2 |
| `posts.csv` | `id,platform,url,author,posted,metric,metric_value,hook_type,format,length,why_it_worked,source_url,checked` | 3 |
| `voices.csv` | `id,kind,text,audience,where,quote,posted,source_url,checked` | 4 |
| `terms.csv` | `id,term,kind,platform,evidence,source_url,checked` | 5 |
| `times.csv` | `id,platform,days,slot_et,evidence,source_url,checked` | 5 |
| `gaps.csv` | `id,gap,audience,evidence,why_open` | 7 |
| `topics.csv` | `id,topic,hook,audience,platform,format,demand,gap,fit,evidence` | 7 |
| `report.md` | The posting plan, written last | 9 |

Id prefixes: accounts `a-`, posts `p-`, voices `v-`, terms `t-`, times
`h-`, gaps `g-`, topics `k-`, each followed by three digits (`a-001`).

Allowed values:

- `audience`: a short code from `brief.md` (for example `a`, `b`, `both`).
- `kind` in `voices.csv`: `question` or `pain`.
- `kind` in `terms.csv`: `hashtag`, `search` (what people type into a
  search box) or `keyword` (words in titles and bios).
- `followers`, `metric_value`: a plain number (`12400`, no commas, no
  "12.4K": write out `12400`) or `not found`, `hidden`, `blocked`.
- `posted`, `followers_as_of`, `checked`: `YYYY-MM-DD`, or `not found`.
- `slot_et`: a time range in US Eastern, `HH:MM-HH:MM` (24 hour).
- `demand`, `gap`, `fit`: whole numbers 1 to 5 (section 7).
- `evidence`: row ids separated by spaces (`p-004 v-012`).

## 3. Depth levels

| Level | Accounts | Posts | Voices | Topics |
|---|---|---|---|---|
| Quick | 10 | 10 | 20 | 20 |
| Full (default) | 30 | 20 | 40 or more | 50 |

The user can ask for Quick. Full is what the README promises.

## 4. The steps

### Step 1. Brief (write `brief.md`)

Ask only for what you can't find in the project (search its memory sheet
first, if it has one). You need:

- **Niche:** one sentence.
- **Audiences:** one line each, with a short code (`a`, `b`).
- **Platforms:** the list, and what the creator posts on each.
- **Goal:** for example leads, sales, signups, followers.
- **Run date** (`run_date: YYYY-MM-DD`), which sets the 90-day window, and
  **depth**.
- **Seed list (optional):** accounts, hashtags, subreddits or competitors
  the user already knows.

Write it as a short markdown file with those labels, then run
`niche_ledger.py init <folder>`.

### Step 2. Accounts and creators (write `accounts.csv`)

1. Search each platform for the niche and each audience's words: platform
   search pages, "top creators" lists, the people big accounts follow and
   tag, YouTube channel pages, GitHub topic and trending pages, newsletters
   and podcasts in the niche.
2. Pick accounts that post for one of the audiences now (a post within the
   last 30 days). Spread them across the platforms in the brief. Include
   small accounts that get unusual engagement, not only the biggest.
3. For each: open its public profile page and copy the follower count shown
   there (`followers`, `followers_as_of` = the date you saw it). If the
   platform hides it, use the count on a public third-party page and link
   that page as `source_url`, or write `hidden`.
4. **Cadence:** count posts visible in the last 30 days and write it as
   `N per week` or `N per month`. **Formats:** the 2 or 3 formats it posts
   most (for example `reel, carousel`, `2-min video`, `text post`, `repo`).
5. `why_relevant`: one short line on why this account matters for the goal.

### Step 3. Best posts of the last 90 days (write `posts.csv`)

1. From the accounts in step 2, and from platform search for the niche's
   terms, collect candidate posts made inside the 90-day window. Open each
   one. Copy its date, the metric the platform shows (views, likes,
   comments, reactions, stars) and its value.
2. Rank candidates against each account's own usual numbers where you can
   (a post at three times its account's median beats a big account's normal
   post), and by the goal (comments that ask about buying or hiring count
   more for a leads goal).
3. Keep the top posts for the depth level. For each, fill the judgement
   columns from what you saw:
   - `hook_type`: one of `question`, `bold claim`, `number`, `before/after`,
     `story`, `mistake`, `how-to`, `contrarian`, `result reveal`, `trend`.
   - `format`: for example `reel`, `short`, `2-min video`, `long video`,
     `carousel`, `text post`, `image`, `thread`, `repo`.
   - `length`: seconds for video (`45s`), words for text (`180w`), slides
     for carousels (`8 slides`).
   - `why_it_worked`: one sentence naming the hook, the promise and the
     proof, in plain words.

### Step 4. Audience questions and pain points (write `voices.csv`)

1. Read comments on the posts from step 3, then Reddit threads, forums,
   Q&A sites, review sites, Facebook groups that are public, and "People
   also ask" boxes, using each audience's own words.
2. Each row is one question or one pain point, in your words in `text`,
   with the person's exact words in `quote`, the place (`where`, for example
   `r/smallbusiness`) and the thread link as `source_url`. Never record who
   said it.
3. When the same question appears again, add a new row for each place it
   appears. The script counts repeats; you don't merge them.

### Step 5. Terms and posting times (write `terms.csv` and `times.csv`)

1. **Terms:** run `suggest.py <folder> "<seed>" ...` (section 8) with the
   niche's words for each audience: it adds the YouTube and Google search
   suggestions people really type. Then add hashtags on the top posts, YouTube search
   suggestions, and words in the titles of the top posts. One row per term
   per platform, with what you saw as `evidence` (for example
   `on 6 of the top 20 posts`, `search suggestion`).
2. **Times:** first the timestamps of the top posts and accounts you
   already collected (when they posted, converted to US Eastern), then
   current published studies of best posting times for each platform. Each
   row names the platform, the days, the slot in ET and its source. When a
   study and the niche's own posts disagree, keep both rows and say so in
   `evidence`.

### Step 6. Verify (separate pass)

Run `niche_ledger.py sample <folder>`. It picks about 1 in 5 rows from each
fact table. Re-open each sampled `source_url` and check the row. Mark the
row `ok` or `fix: <what is wrong>` in a `verified.csv` with columns
`id,result,checked`. Fix every `fix` row in its table. If more than 1 in 10
sampled rows need a fix, re-collect that table.

### Step 7. Gaps and topics (write `gaps.csv` and `topics.csv`)

1. Run `niche_ledger.py tables <folder>`. It counts repeated questions and
   pains, formats and hook types among the top posts, and terms by platform.
2. **Gaps:** a question or pain that comes up again and again (high count
   in the tables) but that no top account answers well (no top post on it,
   or only old, vague or salesy ones). One row per gap, with the rows that
   show both sides as `evidence`, and one line on `why_open`.
3. **Topics:** at least the depth level's number of video topics. Each one
   has a `hook` (the first line said on screen, under 12 words, true and
   specific), the `audience`, the `platform` and `format` it suits, and
   `evidence` ids. Score each 1 to 5:
   - `demand`: how often the audience asks for it (voices count, search
     terms, views on similar posts).
   - `gap`: how badly it's covered today (5 = nobody, 1 = done to death).
   - `fit`: how well the creator can make it and how close it sits to the
     goal (5 = shows the work and leads to the offer).
4. Run `niche_ledger.py rank <folder>`. It scores (`demand x gap x fit`),
   sorts and numbers the topics. Never re-order them by hand.

### Step 8. Check

Run `niche_ledger.py check <folder>` and fix every problem it lists:
missing links or dates, numbers with commas or "K", posts outside the
window, evidence ids that don't exist, scores outside 1 to 5, too few rows
for the depth level.

### Step 9. Write the report (`report.md`)

Run `niche_ledger.py report <folder>`. It writes the tables (every row with
its source link and date) into `report.md`. Then add, at the top:

1. **The answer in five lines:** who to watch, what works, the biggest gap,
   the first three videos to make, when to post.
2. **Per platform:** cadence, formats and the posting slot to start with,
   each pointing to rows.
3. **What not to do:** patterns the evidence says flop or annoy.
4. **Data note:** run date, how many rows, what was blocked or hidden.

### Step 10. Hand-off

Give the user the five-line answer, the top 10 topics with their hooks,
and the folder path. If the social-media skill is installed, it can turn
`topics.csv` into a calendar; the linkedin skill can draft the LinkedIn
posts. Don't write posts in this skill.

## 5. Platform notes

| Platform | Where to look | Watch out for |
|---|---|---|
| LinkedIn | Creator profiles, post pages, the platform's search for posts | Most numbers need a login: use what public post pages show, else `hidden`. Reactions and comments, not views, are public |
| Instagram | Public profile pages, reel pages, hashtag pages | Follower counts on public pages are rounded ("12.4K"): write `12400` and say `rounded` in `why_relevant` or `evidence` |
| YouTube | Search pages, channel `/videos` and `/about` pages, video pages, read with `youtube_read.cjs` (section 8) | Plain web fetches often come back cut off. The script gives each video's exact date and view count, and the subscriber count a channel shows |
| GitHub | Topic pages, trending, repo pages, stars and forks | Stars are the metric; "posted" is the repo's creation or release date |
| Reddit and forums | Threads in the niche's communities | Quote the words only, never usernames |
| X, TikTok, Threads | Public profile and post pages | Often blocked without login: record `blocked` and move on |

## 6. When a page is blocked or empty

Record `blocked` (the page refused you) or `not found` (it loaded but the
value isn't there) and try another public source for the same fact: a
search result snippet, the account's other profiles, a public analytics
page. Never log in, solve captchas, or use paid tools you weren't given.

## 7. Self-check after each table

- Every row has an id with the right prefix, a `source_url` that starts
  with `http`, and a `checked` date.
- Numbers are plain numbers or one of the allowed words.
- Quotes are copied, short and contain no names or handles.
- Posts sit inside the 90-day window.

## 8. The ledger script

`niche_ledger.py` (next to this file) needs only Python 3.
`youtube_read.cjs` (next to it) reads public YouTube pages in a real
browser and prints JSON; it needs Node.js and Playwright with Chromium.

| Command | Does |
|---|---|
| `init <folder>` | Creates the folder and every CSV with its header (never overwrites) |
| `check <folder>` | Lists every rule broken; exits 1 if any |
| `merge <folder>` | Folds part files such as `voices-a.csv` into `voices.csv` and moves them to `parts/` |
| `sample <folder>` | Prints about 1 in 5 rows of each fact table to re-check |
| `tables <folder>` | Writes `tables.md`: repeat counts, formats, hooks, terms |
| `rank <folder>` | Scores and sorts `topics.csv`, adds `score` and `rank` |
| `report <folder>` | Writes the sourced tables into `report.md` below your summary |
| `python3 suggest.py <folder> "<seed>" ...` | Adds YouTube and Google search suggestions for each seed to `terms.csv`, sourced and dated |
| `node youtube_read.cjs <url>` | A search or `/videos` page: the videos on it. A video page: exact date, views, title. An `/about` page: subscribers as shown |

## 9. Running it cheaply (Haiku)

In Claude Code with the plugin installed, four Haiku helpers collect
(accounts, posts, voices, signals) and one verifies. The main conversation
only writes the brief, scores the topics and writes the summary. Without
helpers, follow steps 1 to 10 yourself, one table at a time. Choosing Haiku
as the model keeps it cheap.
