# Power: Web

For websites, landing pages, one-page sites, link pages, trackers and deploys.

## Builds on
**mock-builder** for local-business samples, the **hallmark** design pass where installed, the **writer**
power for the copy.

## Method
1. Brief: who it is for, the one action a visitor should take, the content that exists, the look.
2. Design: one strong layout, real content (no lorem ipsum), a modern sans pair, readable on a phone first.
3. Track visits privately if the user wants numbers: a tag per link (`?from=<source>`) recorded by a
   simple form or analytics the user controls.
4. Check: mobile layout, page speed, links, alt text on every image, https.
5. Deploy only with the user's yes, and say where it lives and how to update it.

## Unslop pass (no AI-looking pages)
Before showing any page, audit it for the tells that make a site look vibecoded, list each with where it
is, then fix them in this order: spacing, colour, icons, copy, type, layout, details, visuals, motion.
Common tells: purple-to-blue gradients, glows and glassy blobs everywhere, emoji used as labels or icons,
shouty or vague copy ("Unlock your potential"), numbered eyebrow labels on every section, uneven spacing,
three identical feature cards, a glossy abstract blob instead of the real product. Set a direction from
the product first (its character, the one or two places colour is spent, one signature detail). If a page
is already good, say so and suggest small refinements instead of a redesign.
For the full method, install unslop by Damir Sokolovsky (CC BY 4.0, github.com/heydamir/unslop):
`claude plugin install unslop --marketplace heydamir/unslop`.

## Done when
It passes the unslop pass, works on a phone, every link and image is checked, the user approved before it went live.
