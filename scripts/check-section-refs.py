#!/usr/bin/env python3
"""Verify that every `file.md` §Section citation resolves to a real heading.

The SKILL.md contract tables route the agent to specific sections of specific rule
files. Nothing enforces that coupling: rename a heading in a rule file and the
citation pointing at it goes stale silently, and the agent reads the whole file
instead of the section it was scoped to.

This checks two things:

  attributed    A citation preceded by a `file.md` reference must name a heading
                that exists IN THAT FILE. This is the check that catches the
                dangerous case: a real heading cited against the wrong file.
  unattributed  A citation with no filename in its paragraph must at least name a
                heading that exists somewhere in the system.

Run from the repo root:

    python3 scripts/check-section-refs.py

Exits nonzero if anything fails, so it works as a pre-commit hook.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Files whose citations get checked.
CITING_GLOBS = ["agents/*/SKILL.md", "CLAUDE.md"]

# Files whose headings count as citable targets.
TARGET_GLOBS = ["agents/*/*.md", "profile/*.md", "experiences/*.md", "research/*.md"]

HEADING_RE = re.compile(r"^#{2,3}\s+(.+?)\s*$")
MD_REF_RE = re.compile(r"`([^`]+\.md)`")
# Citations are not delimited in prose, and headings themselves contain commas
# ("The two readers, reweighted"). So grab a generous window after the § and let
# longest-prefix matching decide where the heading actually ends. The window is a
# lookahead so it stays zero-width: a consuming match would swallow the following
# § in "§Page budget, §Contact header" and silently skip half the citations.
CITATION_RE = re.compile(r"§(?=(.{0,80}))")


def collect_headings():
    """Map each target file to the set of ## / ### headings it defines."""
    headings = {}
    for pattern in TARGET_GLOBS:
        for path in sorted(ROOT.glob(pattern)):
            found = set()
            for line in path.read_text(encoding="utf-8").splitlines():
                match = HEADING_RE.match(line)
                if match:
                    found.add(match.group(1))
            headings[path.resolve()] = found
    return headings


def paragraphs(text):
    """Yield (start_line, paragraph_text) with newlines collapsed to spaces.

    Citations wrap across lines, so matching line-by-line produces false failures
    on a heading split by a line break. Collapsing the paragraph first avoids that
    while start_line keeps the report pointing somewhere useful.
    """
    lines = text.splitlines()
    start = None
    buffer = []
    for number, line in enumerate(lines, 1):
        if line.strip():
            if start is None:
                start = number
            buffer.append(line.strip())
        elif buffer:
            yield start, " ".join(buffer)
            start, buffer = None, []
    if buffer:
        yield start, " ".join(buffer)


def resolve(ref, citing_path):
    """Resolve a `file.md` reference to a real path, or None.

    References are written relative to the citing file (`record-schema.md`,
    `../tailor-resume/jd-analysis.md`) or from the repo root (`profile/skills.md`).
    """
    for base in (citing_path.parent, ROOT):
        candidate = (base / ref).resolve()
        if candidate.is_file():
            return candidate
    return None


def longest_heading_match(tail, candidates):
    """Return the longest heading that prefixes `tail`, or None.

    Headings are not delimited in prose, so `§Page budget, and the one` has to be
    matched by prefix. Longest wins so `§Skills section` is not satisfied by a
    shorter `§Skills` heading that happens to exist elsewhere.
    """
    best = None
    for heading in candidates:
        if tail.startswith(heading) and (best is None or len(heading) > len(best)):
            best = heading
    return best


def main():
    headings = collect_headings()
    every_heading = set().union(*headings.values()) if headings else set()

    citing_files = []
    for pattern in CITING_GLOBS:
        citing_files.extend(sorted(ROOT.glob(pattern)))

    failures = []
    checked = 0
    attributed = 0

    for path in citing_files:
        rel = path.relative_to(ROOT)
        for start_line, text in paragraphs(path.read_text(encoding="utf-8")):
            for match in CITATION_RE.finditer(text):
                tail = match.group(1).strip()

                # `§<Heading>` is documentation describing the citation format,
                # not a citation. Same <angle-bracket> placeholder convention the
                # rest of the repo uses for <company-slug> and <YYYY-MM-DD>.
                if tail.startswith("<"):
                    continue
                checked += 1

                # Attribute the citation to the nearest `file.md` before it.
                refs = [m for m in MD_REF_RE.finditer(text) if m.end() <= match.start()]
                target = None
                if refs:
                    ref = refs[-1].group(1)
                    target = resolve(ref, path)
                    if target is None:
                        failures.append(
                            f"{rel}:{start_line}: §{tail[:40]} cites `{ref}`, "
                            f"which does not exist"
                        )
                        continue

                if target is not None and target in headings:
                    attributed += 1
                    if not longest_heading_match(tail, headings[target]):
                        near = longest_heading_match(tail, every_heading)
                        hint = (
                            f" (§{near} exists, but not in that file)"
                            if near
                            else ""
                        )
                        failures.append(
                            f"{rel}:{start_line}: §{tail[:40]} not found in "
                            f"{target.relative_to(ROOT)}{hint}"
                        )
                elif not longest_heading_match(tail, every_heading):
                    failures.append(
                        f"{rel}:{start_line}: §{tail[:40]} matches no heading anywhere"
                    )

    if failures:
        print(f"{len(failures)} broken section reference(s):\n")
        for failure in failures:
            print(f"  {failure}")
        print(f"\nChecked {checked} citations across {len(citing_files)} files.")
        return 1

    print(
        f"OK: {checked} section citations resolve "
        f"({attributed} checked against a named file)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
