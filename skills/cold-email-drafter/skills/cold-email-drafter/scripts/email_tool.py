#!/usr/bin/env python3
"""Cold email drafter: a 3-email sequence from a site-audit result and a mock link, plus a checker.

    python3 email_tool.py draft --audit audit.json --mock https://site/previews/slug/ \\
        --sender "Your Name" --business "Joe's Plumbing" [--owner Joe] [--city Austin] > emails.txt
    python3 email_tool.py check emails.txt

draft writes plain-text starting drafts (Claude then rewrites the personal line in a human
voice). check fails the sequence if email 1's body is over 90 words, any email has an em dash,
hype words, more than one link, no subject, or no opt-out line, or if the address line is
missing. CAN-SPAM needs your real name, a valid postal address and a working opt-out.
Send emails 2 and 3 as replies in the same thread: their "Re:" subject is only honest there.
"""
import argparse
import json
import re
import sys

ADDRESS = "[[YOUR POSTAL ADDRESS: street, city, country]]"
OPT_OUT = 'Not interested? Reply "no thanks" and I won\'t email again.'
HYPE = ["game-changer", "game changer", "revolutionary", "unlock", "supercharge", "seamless", "elevate",
        "skyrocket", "cutting-edge", "world-class", "guarantee", "100%", "act now", "limited time", "free money",
        "dear sir", "hope this email finds you well", "i hope this finds you well", "synergy", "leverage"]


def first_problem(audit):
    probs = audit.get("problems") or []
    return probs[0]["problem"] if probs else ""


def draft(a):
    audit = json.load(open(a.audit, encoding="utf-8")) if a.audit else {}
    if isinstance(audit.get("score"), int) and audit["score"] < 30:
        print(f"warning: this site scores {audit['score']}/100 (strong already). A pitch about it will feel thin; consider skipping it.", file=sys.stderr)
    hi = f"Hi {a.owner}," if a.owner else "Hi there,"
    p = first_problem(audit)
    where = f" in {a.city}" if a.city else ""
    no_site = any(x.get("id") == "no_website" for x in audit.get("problems", []))
    if no_site:
        personal = f"I searched for {a.business}{where} and couldn't find a website, only directory listings."
    elif p:
        personal = f"I looked at {a.business}'s website and noticed one thing: {p[0].lower() + p[1:]}"
    else:
        personal = f"I came across {a.business}{where} and made you something."
    better = "a one-page site" if no_site else "a cleaner one-page site"
    sign = f"{a.sender}\n{ADDRESS}\n{OPT_OUT}"
    e1 = f"""Subject: {a.business} homepage idea

{hi}

{personal}

So I mocked up {better} for you. Take a look:
{a.mock}

Want it live in 7 days for $400?

{sign}"""
    e2 = f"""Subject: Re: {a.business} homepage idea

{hi}

Quick follow-up on the mockup I made for {a.business}:
{a.mock}

Happy to change anything on it. Want me to make it live?

{sign}"""
    e3 = f"""Subject: Re: {a.business} homepage idea

{hi}

Last note from me. The mockup stays up for a while if you want it later:
{a.mock}

If the timing is wrong, no problem at all.

{sign}"""
    return "\n\n===== EMAIL 1 (day 0) =====\n" + e1 + "\n\n===== EMAIL 2 (day 3) =====\n" + e2 + "\n\n===== EMAIL 3 (day 7) =====\n" + e3 + "\n"


def body_words(email):
    lines = [l for l in email.strip().splitlines() if not l.lower().startswith("subject:")]
    text = "\n".join(lines)
    for tail in (ADDRESS, OPT_OUT):
        text = text.replace(tail, "")
    return len(re.findall(r"\b[\w'$.:/-]+\b", text))


def check(path):
    raw = open(path, encoding="utf-8").read()
    parts = [p for p in re.split(r"=+ EMAIL \d.*?=+", raw) if p.strip()]
    problems = []
    if not parts:
        problems.append("no emails found (separate them with '===== EMAIL 1 (day 0) =====' lines)")
    for i, em in enumerate(parts, 1):
        low = em.lower()
        if not re.search(r"^subject:\s*\S", em, re.I | re.M):
            problems.append(f"email {i}: no subject line")
        if "—" in em:
            problems.append(f"email {i}: has an em dash")
        for w in HYPE:
            if w in low:
                problems.append(f"email {i}: hype or spam phrase '{w}'")
        links = re.findall(r"https?://\S+", em)
        if len(links) > 1:
            problems.append(f"email {i}: {len(links)} links; keep one")
        if not re.search(r"(reply .*(no|stop|unsubscribe)|unsubscribe|opt out|won't email again)", low):
            problems.append(f"email {i}: no one-line opt-out")
        if "[[your postal address" not in low and not re.search(r"\d+ .+,", em.strip().splitlines()[-2] if len(em.strip().splitlines()) > 1 else ""):
            problems.append(f"email {i}: no postal address line (CAN-SPAM)")
        n = body_words(em)
        if i == 1 and n > 90:
            problems.append(f"email 1: body is {n} words; keep it to 90 or fewer")
    if len(parts) > 1:
        print('note: send emails 2 and 3 as replies in the same thread, so "Re:" is true', file=sys.stderr)
    if "[[YOUR POSTAL ADDRESS" in raw:
        print("note: fill in your real postal address before sending", file=sys.stderr)
    if problems:
        print("\n".join(problems))
        return 1
    print(f"ok: {len(parts)} emails pass. Email 1 body: {body_words(parts[0])} words.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("draft")
    d.add_argument("--audit", help="site-audit JSON")
    d.add_argument("--mock", required=True, help="link to the mock")
    d.add_argument("--sender", required=True, help="your real name")
    d.add_argument("--business", required=True)
    d.add_argument("--owner", default="", help="owner's first name, only if public")
    d.add_argument("--city", default="")
    c = sub.add_parser("check")
    c.add_argument("file")
    a = ap.parse_args()
    if a.cmd == "draft":
        sys.stdout.write(draft(a))
    else:
        sys.exit(check(a.file))


if __name__ == "__main__":
    main()
