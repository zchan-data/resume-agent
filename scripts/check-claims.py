#!/usr/bin/env python3
"""Verify the claim fields in every experience record are internally consistent.

A prohibition is only worth having if it is impossible to skip. These records hold
`claim` and `do_not_claim` fields that bind every downstream agent, and nothing else
checks them. The specific failure this exists to prevent was live in the system before
the fields existed: an accomplishment whose prose warned "do not put R² on a resume"
carried `R² 0.56` inside its own `default_bullet`, which is the line most likely to be
copied onto a resume unedited.

Checks, per accomplishment:

  claim present     Every ACC block declares ok | restricted | blocked.
  reason present    restricted and blocked carry a do_not_claim saying what is off limits.
  no stray reason   claim: ok does not carry one, so `ok` keeps meaning "no constraints".
  bullet blocked    A blocked accomplishment's default_bullet says BLOCKED.
  bullet clean      A restricted accomplishment's default_bullet does not repeat a
                    figure its own do_not_claim names.

The last check is deliberately narrow. It considers only decimals, percentages, ratios,
and the metric names themselves — the shapes a reported result actually takes. Bare
integers are ignored because they are nearly always counts, and a `do_not_claim` routinely
names counts in the course of saying they are still allowed. Widening it produced two
false positives for every real finding, and a check that cries wolf gets ignored.

Also checks that frontmatter `claimable` agrees with the accomplishments underneath it.

Run from the repo root:

    python3 scripts/check-claims.py

Exits nonzero if anything fails, so it works as a pre-commit hook.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RECORD_GLOBS = ["experiences/*/*.md"]

ACC_RE = re.compile(r"^###\s+(ACC-\d+)\b.*$")
FIELD_RE = re.compile(r"^-\s+\*\*(\w+)[^:]*:\*\*\s*(.*)$")
CLAIMABLE_RE = re.compile(r"^claimable:\s*(\S+)\s*$", re.MULTILINE)
# Only the shapes a reported result takes: a metric name, a decimal, a percentage, or a
# ratio. Bare integers are excluded on purpose — see the module docstring.
FIGURE_RE = re.compile(r"R²|RMSE|\b\d+\.\d+x?%?|\b\d+(?:\.\d+)?[%x]\b")
VALID_CLAIMS = {"ok", "restricted", "blocked"}
VALID_CLAIMABLE = {"full", "partial", "none"}


def accomplishments(body):
    """Yield (acc_id, line_number, {field: value}) for each ACC block in Claims."""
    lines = body.splitlines()
    current = None
    for number, line in enumerate(lines, 1):
        heading = ACC_RE.match(line)
        if heading:
            if current:
                yield current
            current = (heading.group(1), number, {})
            continue
        if line.startswith("## "):
            if current:
                yield current
            current = None
            continue
        if current:
            field = FIELD_RE.match(line)
            if field:
                current[2][field.group(1)] = field.group(2)
            elif line.startswith("  ") and current[2]:
                last = list(current[2])[-1]
                current[2][last] += " " + line.strip()
    if current:
        yield current


def claims_section(text):
    """Return the text of the ## Claims section, or None."""
    match = re.search(r"^## Claims$(.*?)^## ", text, re.MULTILINE | re.DOTALL)
    return match.group(1) if match else None


def repeats(token, bullet):
    """True when `bullet` reuses `token` as a standalone figure, not as a substring.

    Substring matching finds `0` inside `80%` and every check after that is noise.
    """
    return re.search(rf"(?<![\w.]){re.escape(token)}(?![\w.])", bullet) is not None


def main():
    failures = []

    records = 0

    paths = []
    for pattern in RECORD_GLOBS:
        paths.extend(sorted(ROOT.glob(pattern)))

    for path in paths:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        body = claims_section(text)
        if body is None:
            failures.append(f"{rel}: no `## Claims` section")
            continue
        records += 1

        declared = CLAIMABLE_RE.search(text)
        if not declared:
            failures.append(f"{rel}: frontmatter has no `claimable`")
        elif declared.group(1) not in VALID_CLAIMABLE:
            failures.append(
                f"{rel}: claimable is {declared.group(1)!r}, "
                f"expected one of {sorted(VALID_CLAIMABLE)}"
            )

        seen = []
        for acc, line, fields in accomplishments(body):
            where = f"{rel}:{line}: {acc}"
            claim = fields.get("claim", "").strip()
            reason = fields.get("do_not_claim", "").strip()
            bullet = fields.get("default_bullet", "")

            if not claim:
                failures.append(f"{where} has no `claim` field")
                continue
            if claim not in VALID_CLAIMS:
                failures.append(
                    f"{where} claim is {claim!r}, expected one of {sorted(VALID_CLAIMS)}"
                )
                continue
            seen.append(claim)

            if claim in {"restricted", "blocked"} and not reason:
                failures.append(f"{where} is {claim} but has no `do_not_claim`")
            if claim == "ok" and reason:
                failures.append(
                    f"{where} is ok but carries a `do_not_claim` — "
                    f"use restricted, or drop the field"
                )
            if claim == "blocked" and "BLOCKED" not in bullet:
                failures.append(
                    f"{where} is blocked but its default_bullet is not marked BLOCKED"
                )
            if claim == "restricted" and bullet:
                hit = sorted({t for t in FIGURE_RE.findall(reason) if repeats(t, bullet)})
                if hit:
                    failures.append(
                        f"{where} default_bullet repeats {', '.join(hit)}, "
                        f"which its own do_not_claim names"
                    )

        if declared and seen:
            actual = (
                "none"
                if all(c == "blocked" for c in seen)
                else "full"
                if all(c == "ok" for c in seen)
                else "partial"
            )
            if declared.group(1) != actual:
                failures.append(
                    f"{rel}: claimable is {declared.group(1)!r} but the "
                    f"accomplishments say {actual!r}"
                )

    if failures:
        print(f"{len(failures)} claim-consistency failure(s):\n")
        for failure in failures:
            print(f"  {failure}")
        return 1

    print(f"OK: claim fields consistent across {records} record(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
