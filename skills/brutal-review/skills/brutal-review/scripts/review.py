#!/usr/bin/env python3
"""Brutal Review: a blunt, structured critique of a plan, pitch, resume or code from a
DIFFERENT model than the one you are working with.

    python3 review.py plan.md --style headchef
    python3 review.py pitch.md --context notes.md --provider openai --model gpt-4o --md out.md
    python3 review.py plan.md --dry-run          show what would be sent, send nothing
    python3 review.py plan.md --second-pass      the reviewer drops weak points, adds missed ones

Providers: openai, xai, anthropic, google, ollama (local), claude (the claude CLI), fake (tests).
Keys come only from environment variables: OPENAI_API_KEY, XAI_API_KEY, ANTHROPIC_API_KEY,
GOOGLE_API_KEY. With no --provider, the first key found wins; with none, the claude CLI.
Before anything is sent, emails, phone numbers and things that look like keys are replaced.
Output: validated JSON on stdout (and markdown with --md). Exit 1 with a plain message on errors.
Standard library only.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

MAX_CHARS = 120_000
STYLES = {
    "devil": "Argue the other side. Assume the author is wrong and build the strongest case that this will not work. Name the assumption each weakness rests on.",
    "redteam": "Attack it like an adversary: find where it breaks, who can exploit it, what fails under load, what a competitor or a bad actor would do first.",
    "headchef": "Review it like a demanding head chef inspecting a plate before it leaves the kitchen: short sentences, no softening, no praise unless it is earned, and every complaint comes with the exact fix.",
}
DEFAULT_MODELS = {"openai": "gpt-4o", "xai": "grok-3", "anthropic": "claude-sonnet-5-5",
                  "google": "gemini-2.5-pro", "ollama": "llama3.1", "claude": "", "fake": "fake"}
KEYS = {"openai": "OPENAI_API_KEY", "xai": "XAI_API_KEY", "anthropic": "ANTHROPIC_API_KEY", "google": "GOOGLE_API_KEY"}
SCHEMA_TEXT = ('Reply with JSON only, no prose around it, exactly this shape: {"verdict": "one sentence", '
               '"score": integer 1 to 100 (most real work scores 30 to 60), "weaknesses": [{"severity": '
               '"critical" | "major" | "minor", "issue": "what is wrong", "fix": "the concrete change"}], '
               '"fails_in_6_months_because": "the single most likely reason"}. List the most important '
               'weaknesses first, 3 to 10 of them.')

REDACTIONS = [
    ("key", re.compile(r"(sk-[A-Za-z0-9_-]{16,}|xai-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|xox[abp]-[A-Za-z0-9-]{10,}|Bearer\s+[A-Za-z0-9._-]{16,})")),
    ("email", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("phone", re.compile(r"(?<![\w-])\+?\d[\d ().-]{8,}\d(?![\w-])")),
]


class Fail(Exception):
    pass


def redact(text):
    counts = {}
    for name, rx in REDACTIONS:
        def sub(m, name=name):
            if name == "phone" and sum(c.isdigit() for c in m.group(0)) < 10:
                return m.group(0)
            counts[name] = counts.get(name, 0) + 1
            return f"[{name} removed]"
        text = rx.sub(sub, text)
    return text, counts


def read_text(path):
    try:
        raw = open(path, "rb").read()
    except OSError as e:
        raise Fail(f"Can't read {path}: {e.strerror or e}")
    if b"\x00" in raw[:4096]:
        raise Fail(f"{path} looks like a binary file. Give a text, markdown or code file.")
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", "replace")


def pick_provider(name):
    if name:
        return name
    for p, k in KEYS.items():
        if os.environ.get(k):
            return p
    return "claude"


def post(url, body, headers, timeout, tries=4):
    data = json.dumps(body).encode()
    for attempt in range(tries):
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(2 ** attempt * 2)
                continue
            detail = e.read()[:300].decode("utf-8", "replace") if hasattr(e, "read") else ""
            raise Fail(f"The provider said HTTP {e.code}. {detail}".strip())
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            if attempt < tries - 1:
                time.sleep(2 ** attempt)
                continue
            raise Fail(f"Couldn't reach the provider: {getattr(e, 'reason', e)}")
        except json.JSONDecodeError:
            raise Fail("The provider sent back something that isn't JSON.")


def ask(provider, model, system, user, timeout):
    """Return the model's raw text reply."""
    if provider in KEYS and not os.environ.get(KEYS[provider]):
        raise Fail(f"Set {KEYS[provider]} in your environment to use {provider}. Never paste keys into a chat.")
    try:
        if provider in ("openai", "xai"):
            base = "https://api.openai.com/v1" if provider == "openai" else "https://api.x.ai/v1"
            r = post(f"{base}/chat/completions", {"model": model, "temperature": 0.4,
                     "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]},
                     {"Authorization": "Bearer " + os.environ[KEYS[provider]]}, timeout)
            return r["choices"][0]["message"]["content"]
        if provider == "anthropic":
            r = post("https://api.anthropic.com/v1/messages", {"model": model, "max_tokens": 2500, "system": system,
                     "messages": [{"role": "user", "content": user}]},
                     {"x-api-key": os.environ[KEYS[provider]], "anthropic-version": "2023-06-01"}, timeout)
            return "".join(b.get("text", "") for b in r["content"])
        if provider == "google":
            r = post(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                     {"systemInstruction": {"parts": [{"text": system}]}, "contents": [{"role": "user", "parts": [{"text": user}]}],
                      "generationConfig": {"responseMimeType": "application/json"}},
                     {"x-goog-api-key": os.environ[KEYS[provider]]}, timeout)
            return r["candidates"][0]["content"]["parts"][0]["text"]
        if provider == "ollama":
            host = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
            r = post(f"{host}/api/chat", {"model": model, "stream": False, "format": "json",
                     "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}, {}, timeout)
            return r["message"]["content"]
        if provider == "claude":
            exe = shutil.which("claude")
            if not exe:
                raise Fail("No API key found and the claude CLI isn't installed. Set a provider key, or install Claude Code.")
            cmd = [exe, "-p", system + "\n\n" + user] + (["--model", model] if model else [])
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if r.returncode != 0:
                raise Fail("The claude CLI failed: " + (r.stderr or r.stdout).strip()[:300])
            return r.stdout
        if provider == "fake":
            if os.environ.get("BRUTAL_FAKE_SLEEP"):
                time.sleep(float(os.environ["BRUTAL_FAKE_SLEEP"]))
                if float(os.environ["BRUTAL_FAKE_SLEEP"]) > timeout:
                    raise Fail("The provider timed out.")
            return os.environ.get("BRUTAL_FAKE_RESPONSE", "")
    except (KeyError, IndexError, TypeError):
        raise Fail(f"{provider} answered in a shape this script doesn't understand.")
    except subprocess.TimeoutExpired:
        raise Fail("The provider timed out.")
    raise Fail(f"Unknown provider {provider!r}. Use one of: {', '.join(DEFAULT_MODELS)}")


def parse(text):
    """Pull the JSON object out of the reply and check it has the right shape."""
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        raise ValueError("no JSON object in the reply")
    d = json.loads(m.group(0))
    if not isinstance(d.get("verdict"), str) or not d["verdict"].strip():
        raise ValueError("missing verdict")
    score = d.get("score")
    if isinstance(score, str) and score.strip().isdigit():
        score = int(score)
    if not isinstance(score, (int, float)) or not 1 <= score <= 100:
        raise ValueError("score must be 1 to 100")
    d["score"] = int(score)
    ws = d.get("weaknesses")
    if not isinstance(ws, list) or not ws:
        raise ValueError("no weaknesses listed")
    order = {"critical": 0, "major": 1, "minor": 2}
    clean = []
    for w in ws:
        if not isinstance(w, dict) or str(w.get("severity", "")).lower() not in order or not w.get("issue") or not w.get("fix"):
            raise ValueError("each weakness needs severity, issue and fix")
        clean.append({"severity": w["severity"].lower(), "issue": str(w["issue"]), "fix": str(w["fix"])})
    d["weaknesses"] = sorted(clean, key=lambda w: order[w["severity"]])
    if not isinstance(d.get("fails_in_6_months_because"), str):
        raise ValueError("missing the 6-month failure reason")
    return {k: d[k] for k in ("verdict", "score", "weaknesses", "fails_in_6_months_because")}


def review(provider, model, system, user, timeout):
    text = ask(provider, model, system, user, timeout)
    try:
        return parse(text)
    except (ValueError, json.JSONDecodeError) as e:
        retry = ask(provider, model, system, user + f"\n\nYour last reply was not valid ({e}). " + SCHEMA_TEXT, timeout)
        try:
            return parse(retry)
        except (ValueError, json.JSONDecodeError) as e2:
            raise Fail(f"The reviewer didn't return a valid critique twice ({e2}). Nothing was made up; try again or another provider.")


def markdown(r, provider, model):
    lines = [f"## Brutal Review ({provider}{', ' + model if model else ''})", "", f"**Verdict:** {r['verdict']}", "",
             f"**Score:** {r['score']}/100", "", "**Weaknesses**", ""]
    for i, w in enumerate(r["weaknesses"], 1):
        lines.append(f"{i}. [{w['severity']}] {w['issue']}  \n   Fix: {w['fix']}")
    lines += ["", f"**Most likely reason it fails in 6 months:** {r['fails_in_6_months_because']}", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="A blunt, structured critique from a different model.")
    ap.add_argument("file", help="the plan, pitch, resume or code to review (text file)")
    ap.add_argument("--context", action="append", default=[], help="extra files for context (repeatable)")
    ap.add_argument("--style", choices=sorted(STYLES), default="headchef")
    ap.add_argument("--provider", choices=sorted(DEFAULT_MODELS))
    ap.add_argument("--model", help="the provider's model name (defaults can age: check your provider)")
    ap.add_argument("--second-pass", action="store_true", help="ask the reviewer to drop weak points and add missed ones")
    ap.add_argument("--timeout", type=float, default=180)
    ap.add_argument("--dry-run", action="store_true", help="print what would be sent and stop")
    ap.add_argument("--md", help="also write the critique as markdown")
    a = ap.parse_args()
    try:
        body = read_text(a.file)
        if not body.strip():
            raise Fail("The file is empty. Give it the plan, pitch, resume or code to review.")
        ctx = "".join(f"\n\n--- Context: {os.path.basename(c)} ---\n{read_text(c)}" for c in a.context)
        text, counts = redact(f"--- To review: {os.path.basename(a.file)} ---\n{body}{ctx}")
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS] + "\n\n[cut here: the input was longer than this tool sends]"
            print(f"note: input cut to {MAX_CHARS} characters", file=sys.stderr)
        provider = pick_provider(a.provider)
        model = a.model if a.model is not None else DEFAULT_MODELS[provider]
        if provider in KEYS and not os.environ.get(KEYS[provider]):
            raise Fail(f"Set {KEYS[provider]} in your environment to use {provider}. Never paste keys into a chat.")
        removed = ", ".join(f"{n} {k}{'s' if n > 1 else ''}" for k, n in counts.items()) or "nothing"
        print(f"sending {len(text):,} characters to {provider}{' (' + model + ')' if model else ''}; removed: {removed}", file=sys.stderr)
        if provider == "claude":
            print("note: no other provider key found, so this uses the claude CLI: the same model family, a weaker second opinion", file=sys.stderr)
        system = ("You are an outside reviewer with no stake in this work. " + STYLES[a.style] +
                  " Judge the substance: will it work, and what will break it. " + SCHEMA_TEXT)
        if a.dry_run:
            print(json.dumps({"provider": provider, "model": model, "system": system, "user": text}, indent=2))
            return 0
        result = review(provider, model, system, text, a.timeout)
        if a.second_pass:
            again = (text + "\n\n--- Your first critique ---\n" + json.dumps(result) +
                     "\n\nReview your own critique: drop any point that is weak or wrong, add anything important you missed, re-score.")
            result = review(provider, model, system, again, a.timeout)
        out = {"provider": provider, "model": model, "style": a.style, **result}
        if a.md:
            open(a.md, "w", encoding="utf-8").write(markdown(result, provider, model))
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return 0
    except Fail as e:
        print(f"brutal-review: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("brutal-review: stopped", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
