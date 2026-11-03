---
name: ai-resume
description: Build a true, one-page, ATS-safe resume (HTML + PDF) for a target role, then run Hallmark design checks and a humanizer pass. Use when asked to "make a resume", "update my CV", "resume for <role>", or to prepare a job application.
---
# AI Resume
Build one page that a recruiter can skim in 6 seconds and an ATS can parse cleanly. Every claim must be true.
## 1. Facts first (never invent)
- Collect facts from the user, their Naukri/LinkedIn profile, and their project files.
- Allowed: real titles, dates, schools, projects, links, and numbers the user can back up.
- Not allowed: invented degrees, employers, dates, metrics, "led a team of X", or a certification they don't hold.
- Missing fact: leave the line out and list it under "Missing facts" in your reply.
## 2. Structure (one page)
1. Name, then one line of contact info: city · phone · email · links (GitHub, site, LinkedIn).
2. A headline aimed at the role, e.g. "AI Generalist | Founder's Office | Builds AI agents with Claude".
3. Summary: 2-3 lines of what you build and for whom.
4. Projects / experience, newest first. For each: title, org, dates, then 2-3 bullets of the form action + tool + result. Use real numbers only ("230+ personalized email drafts", "19 open-source Claude skills").
5. Skills, grouped: AI (Claude, prompting, agents, automation), Build (Python, HTML/CSS), Growth (content, outreach, D2C).
6. Education.
## 3. Build
- One self-contained HTML file with inline CSS, A4 size: `@page{size:A4;margin:14mm}`.
- Use real text only: no text inside images, no tables for layout, single column, so the ATS can read it.
- Use a system font stack or one Google font. Body 10-10.5pt, headings 12-13pt, line-height 1.35.
- Render the PDF with Edge headless, then poll until the file exists:
  `msedge --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=<out.pdf> file:///<resume.html>`
- Check the PDF is exactly 1 page. If it runs over, cut words, not font size.
## 4. Hallmark checks (all must pass)
- [ ] No stock-template tells: no skill bars or star ratings, no "proficiency %", no icon clutter, no photo unless asked, no two-column sidebar.
- [ ] Clear hierarchy: name, then headline, then sections. One accent colour at most, and it meets 4.5:1 contrast on body text.
- [ ] Spacing is consistent (one scale, e.g. 4/8/12/16pt) and every bullet is aligned.
- [ ] Links are written out in full or labelled, and they still work in the PDF.
- [ ] Nothing is cut off or orphaned at the page bottom, and there is no blank second page.
- [ ] Copying all the PDF text gives clean reading order (the ATS test).
## 5. Humanizer pass
- No em dashes. Use commas, colons or full stops.
- Cut AI-slop words: leverage, spearheaded, synergy, passionate, dynamic, results-driven, cutting-edge, seamless.
- Start every bullet with a plain verb: built, sold, wrote, ran, shipped.
- Read it aloud. If a line sounds like a template, rewrite it.
## 6. Output
- `resume.html` and `<Name>-Resume.pdf` in the job folder.
- In your reply, include:
  - the Hallmark checklist with a pass or fail for each item
  - the "Missing facts" list
  - a 1-line headline and a 3-line summary the user can paste into job portals
