#!/usr/bin/env python3
"""Repo check: run before every push. Exits 1 on any failure.

    python3 scripts/check.py

Checks: every skill and tool has a README and a catalog.json row; every image has alt
text; no em dashes; no old brand names; nothing that looks like a key or token; no file
over 5 MB (big media goes in GitHub Releases).
"""
import codecs
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXT = {".md", ".txt", ".json", ".yml", ".yaml", ".html", ".css", ".js", ".mjs", ".py", ".svg", ".sh"}
PROSE = {".md", ".txt", ".html", ".svg", ".yml", ".yaml"}
SKIP_DIRS = {".git", "node_modules", ".fonts", "__pycache__", ".venv"}
# Old brand names, stored rot13 so this file doesn't trip its own check.
OLD_BRANDS = [codecs.decode(w, "rot13") for w in ("fbyvqfsbelbh", "fbyvqf sbe lbh", "sbhaqrejvgunof", "zbarlzbzragf")]
SECRETS = re.compile(r"(sk-[A-Za-z0-9_-]{20,}|ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|xox[abp]-[A-Za-z0-9-]{10,})")
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I)
MD_IMG = re.compile(r"!\[([^\]]*)\]\(")

errors = []


def files():
    for p in ROOT.rglob("*"):
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & SKIP_DIRS):
            yield p


for p in files():
    rel = p.relative_to(ROOT).as_posix()
    if p.stat().st_size > 5 * 1024 * 1024:
        errors.append(f"{rel}: over 5 MB, put it in a GitHub Release")
    if p.suffix not in TEXT:
        continue
    body = p.read_text(encoding="utf-8", errors="replace")
    low = body.lower()
    # Prose only: some scripts and test fixtures hold em dashes on purpose (to detect them).
    if chr(0x2014) in body and p.suffix in PROSE and not rel.startswith("tests/fixtures/"):
        errors.append(f"{rel}: em dash found, rewrite the sentence")
    if rel != "scripts/check.py":
        for word in OLD_BRANDS:
            if word in low:
                errors.append(f"{rel}: old brand name found")
    if SECRETS.search(body):
        errors.append(f"{rel}: looks like a key or token")
    if p.suffix == ".md":
        for tag in IMG_TAG.findall(body):
            m = re.search(r'alt="([^"]*)"', tag)
            if not m or not m.group(1).strip():
                errors.append(f"{rel}: image without alt text: {tag[:60]}")
        for alt in MD_IMG.findall(body):
            if not alt.strip():
                errors.append(f"{rel}: markdown image without alt text")

catalog = json.loads((ROOT / "catalog.json").read_text())
listed = {item["path"] for item in catalog["items"]}
for item in catalog["items"]:
    if not (ROOT / item["path"] / "README.md").exists():
        errors.append(f"catalog.json: {item['path']} has no README.md")
for kind in ("skills", "tools"):
    for d in sorted((ROOT / kind).iterdir()):
        if d.is_dir():
            rel = d.relative_to(ROOT).as_posix()
            if not (d / "README.md").exists():
                errors.append(f"{rel}: missing README.md")
            if rel not in listed:
                errors.append(f"{rel}: missing from catalog.json")

if errors:
    print("\n".join(errors))
    print(f"\n{len(errors)} problem(s). Fix them before you push.")
    sys.exit(1)
print("check passed")
