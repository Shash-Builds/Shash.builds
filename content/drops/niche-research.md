# Drop: Niche Research (free Claude skill)

Ready-to-post copy for the launch. Every number below comes from the real run in
`research/niche/shash-builds/`. Run each one through the humanizer before posting,
and read each community's rules first (see `research/communities.md`).

Links:
- Skill: https://github.com/Shash-Builds/shash.builds/tree/main/skills/niche-research
- Real report: https://github.com/Shash-Builds/shash.builds/blob/main/research/niche/shash-builds/report.md

## LinkedIn (daily log)

I asked Claude to research my own niche before I plan another post.

Not "give me ideas". Real research, with a link and a date on every row.

What came back:
- 33 accounts worth watching
- the 24 best posts of the last 90 days, and why each worked
- 63 questions and complaints from real owners and designers
- 50 video topics, ranked

The finding that changed my plan:
Owners keep getting burned by designers who take the money and go quiet. Hidden hosting fees. Sites that never ship.

None of the 24 best posts talks to the owner about it. They all teach people how to sell websites.

So my next video is the one nobody makes: what a small business website really costs per year.

The skill is free and open source. It runs on Claude's cheapest model.
Link in the comments.

## Instagram reel (caption)

I had Claude research my niche. Every row has a source link.

The gap it found: owners get burned by web designers and nobody explains what a fair project looks like.

So that's what I'm making next. The research skill is free, link in bio.

#webdesign #smallbusiness #claudeai #buildinpublic #freelance

## Reddit: r/ClaudeAI (check the self-promotion rules first)

**Title:** I made a free skill that researches a content niche and links a source for every claim

I kept getting "top creators" lists from Claude with follower counts from who knows when. So I wrote a skill that makes it show its work.

How it works:
- Haiku helpers collect accounts, posts from the last 90 days, audience questions and search terms
- a script rejects any row without a link and a date, and any "best post" older than 90 days
- a separate Haiku pass re-opens a sample of rows (my run: 85 checked, 71 matched, 5 fixed, 9 blocked)
- the main model only scores the topics and writes the plan

Search terms come from YouTube and Google search suggestions, so they're what people type, not a hashtag blog.

Honest limits: Instagram, LinkedIn and Reddit block most logged-out reads, so those tables come out thin. It never logs in or gets around blocks.

Repo (MIT): https://github.com/Shash-Builds/shash.builds/tree/main/skills/niche-research
My own run, so you can see the output: https://github.com/Shash-Builds/shash.builds/blob/main/research/niche/shash-builds/report.md

Happy to hear what breaks.

## GitHub release blurb

Niche Research researches a content niche into a posting plan: top accounts, the best posts of the last 90 days and why, audience questions, content gaps, 50 ranked topics with hooks, posting times in ET and real search terms. Every row has a source link and a date.
