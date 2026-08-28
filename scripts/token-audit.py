#!/usr/bin/env python3
"""Measure what one tailor-resume run loads, scoped vs unscoped.

Reconstructs the reads named in agents/tailor-resume/SKILL.md's contract table.

  scoped   = exactly the sections each step declares
  unscoped = the same files read whole, each distinct file counted ONCE
             (generous to the unscoped side, so the reduction is conservative)

Char counts always run. Token counts run only with Anthropic credentials, via
messages.count_tokens -- never tiktoken, which is OpenAI's tokenizer and
undercounts Claude by ~15-20%.

Usage:  python3 token_audit.py [--model claude-opus-5]
"""
import argparse
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECORDS = ["experiences/jobs", "experiences/projects"]

MISSING = []


def read_whole(rel):
    """Return file contents, or empty string if absent.

    profile/ and experiences/ are gitignored, so a fresh clone has neither.
    Skipping keeps the run honest instead of crashing: both corpora lose the
    same file, and the summary reports what was missing.
    """
    path = os.path.join(REPO, rel)
    if not os.path.exists(path):
        MISSING.append(rel)
        return ""
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def read_sections(rel_paths, sections):
    """Call the repo's own section reader -- the tool the contract assumes."""
    present = [p for p in rel_paths if os.path.exists(os.path.join(REPO, p))]
    for p in rel_paths:
        if p not in present:
            MISSING.append(p)
    if not present:
        return ""
    cmd = [sys.executable, "scripts/read-section.py"]
    for s in sections:
        cmd += ["-s", s]
    cmd += present
    out = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(f"read-section failed for {present} {sections}:\n{out.stderr}")
    return out.stdout


def record_files():
    files = []
    for d in RECORDS:
        full = os.path.join(REPO, d)
        if not os.path.isdir(full):
            continue
        for name in sorted(os.listdir(full)):
            if name.endswith(".md"):
                files.append(os.path.join(d, name))
    return files


def build():
    recs = record_files()
    scoped, unscoped_files = [], []

    def whole(rel):
        scoped.append(read_whole(rel))
        unscoped_files.append(rel)

    def scoped_only(rel, *sections):
        scoped.append(read_sections([rel], list(sections)))
        unscoped_files.append(rel)

    # Step 2 -- analyze the JD
    whole("agents/tailor-resume/jd-analysis.md")

    # Step 3 -- retrieve evidence
    whole("experiences/INDEX.md")
    scoped.append(read_sections(recs, ["Claims"]))
    unscoped_files.extend(recs)
    scoped_only("profile/identity.md", "Career stage")

    # Step 4 -- select and map
    whole("agents/tailor-resume/selection-rules.md")

    # Step 5 -- write the draft
    scoped_only(
        "agents/tailor-resume/format-rules.md",
        "Non-negotiable ATS rules", "Page budget",
        "New grad and student (default)", "Contact header", "Never do",
    )
    scoped_only(
        "agents/tailor-resume/writing-rules.md",
        "The bullet formula", "Bullet order within an entry", "Recomposition",
        "Mechanics", "Truthfulness",
        "Summary section", "Skills section", "Education", "Projects",
    )
    scoped_only("profile/identity.md", "Contact", "Logistics")
    scoped_only("profile/skills.md", "Inventory", "Claimed but unevidenced")
    whole("profile/education.md")

    # Step 7 -- render
    whole("agents/tailor-resume/render.md")
    scoped_only("agents/tailor-resume/format-rules.md", "Whitespace and typography")

    # Unscoped: each distinct file once, read whole
    seen, unscoped = set(), []
    for rel in unscoped_files:
        if rel not in seen:
            seen.add(rel)
            unscoped.append(read_whole(rel))

    return "\n".join(scoped), "\n".join(unscoped), len(recs), len(seen)


def count_tokens(text, model):
    try:
        import anthropic
    except ImportError:
        return None, "anthropic SDK not installed (pip3 install anthropic)"
    try:
        client = anthropic.Anthropic()
        r = client.messages.count_tokens(
            model=model, messages=[{"role": "user", "content": text}]
        )
        return r.input_tokens, None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="claude-opus-5")
    args = ap.parse_args()

    scoped, unscoped, n_recs, n_files = build()
    print(f"One tailor-resume run: {n_files} distinct files, {n_recs} experience records")
    if MISSING:
        print(f"  skipped {len(set(MISSING))} absent file(s): {', '.join(sorted(set(MISSING)))}")
        print("  (experiences/ and profile/ are gitignored -- supply your own data)")
    print()

    sc, uc = len(scoped), len(unscoped)
    if not uc:
        print("Nothing to measure -- no data files present.")
        return 2
    print("CHARACTERS")
    print(f"  unscoped (whole files) : {uc:>9,}")
    print(f"  scoped   (contract)    : {sc:>9,}")
    print(f"  reduction              : {100 * (1 - sc / uc):>8.1f}%\n")

    st, err1 = count_tokens(scoped, args.model)
    ut, err2 = count_tokens(unscoped, args.model)
    if st is None or ut is None:
        print(f"TOKENS: unavailable -- {err1 or err2}")
        print("        (set ANTHROPIC_API_KEY, or run `ant auth login`)")
        return 2

    print(f"TOKENS ({args.model}, via messages.count_tokens)")
    print(f"  unscoped (whole files) : {ut:>9,}")
    print(f"  scoped   (contract)    : {st:>9,}")
    print(f"  reduction              : {100 * (1 - st / ut):>8.1f}%")
    print(f"  tokens saved per run   : {ut - st:>9,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
