#!/usr/bin/env python3
"""Print named sections of a markdown file, instead of the whole file.

The SKILL.md contract tables scope each step to specific sections. Nothing made
that real: `Read` loads an entire file, so a step scoped to two sections of
`writing-rules.md` still paid for all of it, and the head/tail split in an
experience record saved nothing.

This is the mechanism the contracts assume. Frontmatter is always included when
present, because retrieval decisions depend on it.

    python3 scripts/read-section.py -s "The bullet formula" -s Mechanics \\
        agents/tailor-resume/writing-rules.md

    python3 scripts/read-section.py -s Claims experiences/jobs/*.md

    python3 scripts/read-section.py --list agents/write-cover-letter/voice-rules.md

Multiple files are allowed, which is the point for experience records: one call
returns the claim blocks for every shortlisted record and none of their prose.

Exits nonzero if a requested section is missing from a file, so a renamed
heading fails loudly here the same way it does in check-section-refs.py.
"""

import argparse
import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def split_frontmatter(lines):
    """Return (frontmatter_lines, body_lines). Frontmatter is [] when absent."""
    if not lines or lines[0].strip() != "---":
        return [], lines
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[: index + 1], lines[index + 1 :]
    # Unterminated fence is not frontmatter.
    return [], lines


def headings(body):
    """Yield (index, level, text) for every heading line in `body`."""
    fenced = False
    for index, line in enumerate(body):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = HEADING_RE.match(line)
        if match:
            yield index, len(match.group(1)), match.group(2)


def extract(body, wanted):
    """Return the lines of the section titled `wanted`, heading included.

    A section runs to the next heading at the same or a higher level, so asking
    for `## Claims` returns its `### ACC-001` children too.
    """
    marks = list(headings(body))
    for position, (index, level, text) in enumerate(marks):
        if text != wanted:
            continue
        end = len(body)
        for next_index, next_level, _ in marks[position + 1 :]:
            if next_level <= level:
                end = next_index
                break
        return body[index:end]
    return None


def main():
    parser = argparse.ArgumentParser(
        description="Print named sections of a markdown file rather than all of it."
    )
    parser.add_argument(
        "-s",
        "--section",
        action="append",
        default=[],
        metavar="HEADING",
        help="exact heading text, without the leading #. Repeatable.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="list available headings instead of printing content",
    )
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()

    if not args.section and not args.list:
        parser.error("give at least one --section, or --list")

    missing = []
    unreadable = []
    multiple = len(args.files) > 1

    for path in args.files:
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError as error:
            unreadable.append(f"{path}: {error.strerror}")
            continue

        front, body = split_frontmatter(lines)

        if args.list:
            print(f"=== {path} ===")
            for _, level, text in headings(body):
                print(f"{'  ' * (level - 1)}{text}")
            print()
            continue

        chunks = []
        for wanted in args.section:
            found = extract(body, wanted)
            if found is None:
                missing.append(f"{path}: no section titled {wanted!r}")
            else:
                chunks.append(found)

        if not chunks:
            continue

        if multiple:
            print(f"=== {path} ===")
        if front:
            print("\n".join(front))
            print()
        for chunk in chunks:
            print("\n".join(chunk).rstrip())
            print()

    for problem in unreadable + missing:
        print(f"error: {problem}", file=sys.stderr)
    if unreadable or missing:
        available = args.files[0]
        print(
            f"hint: python3 scripts/read-section.py --list {available}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
