#!/usr/bin/env python3
"""Predict how much of the page a draft `resume.md` will fill, before rendering.

The draft is approved at a gate that shows the user markdown, and markdown has no
pages. So the property a recruiter judges first, whether the page looks full, is
invisible at exactly the moment it is decided. It surfaces only once the PDF exists,
which is after approval, which costs a revision round: the draft comes back to be
filled with real evidence that was cut from it earlier. Observed drafts have landed
anywhere from 1.5in of dead space to two thirds of a page.

This closes the gap without a render. It parses the markdown, predicts the rendered
height, and reports any shortfall in the unit the writer controls: bullets.

    python3 scripts/estimate-fill.py resumes/<slug>/resume.md

Exits nonzero when the draft is predicted short or long, so step 5 cannot reach the
approval gate without the number having been looked at.

## How it predicts

Line wrapping is computed from Helvetica glyph widths, not character counts. Character
counting was tried first and is not good enough: a bullet of 230 characters and one of
233 render to three lines and two lines respectively, because capitals and digits are
far wider than `i`, `l`, and `t`. Over a calibration set of 124 real bullets, glyph
widths mispredict 4 and character counting mispredicts 6 at its best-tuned width, and
the glyph model's errors sit on genuinely marginal lines rather than scattered.

Vertical spacing is a single measured constant per line rather than one per SPACE_*
value in the template. The template's gaps differ by only a point or two at this scale,
and modelling each separately fit worse, because the residual is dominated by wrap
prediction rather than by spacing.

## It is an estimate

Calibration residuals run to about 3 lines on the worst case and under 2 on most, so
the useful resolution is a couple of lines. It answers "is this draft materially short"
and not "is this draft one line short." A result sitting on a threshold means render it
and look. The rendered PDF stays ground truth; this is a forecast, not a
replacement for the page-count check in `render.md` §Verification or for looking at the
page. Treat a result within a line of a threshold as "render it and see."

Of the two ways to be wrong, over-predicting height is the worse one: it calls a short
page full and ships the exact defect this script exists to prevent. Under-predicting
sends the agent looking for another bullet and risks a spill to page two, which the
page-count check catches in seconds. Preserve that asymmetry if the constants are refit.

## Coupling

Every constant is calibrated to the current values in `templates/resume-style.typ`
(BODY_SIZE 10pt, MARGIN 0.5in, the SPACE_* rhythm, and the Helvetica font stack).
Change those and this drifts silently. `--calibrate` re-measures against whatever
rendered PDFs are in `resumes/` and reports the residuals; run it after touching the
template. `resumes/` is gitignored, so a fresh clone has nothing to calibrate against
until it has generated some, and the shipped constants are the ones to start from.
"""

import math
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Geometry, mirroring templates/resume-style.typ ---

PAGE_HEIGHT = 792.0  # us-letter
PAGE_WIDTH = 612.0
MARGIN = 36.0  # 0.5in
TEXT_BLOCK = PAGE_HEIGHT - 2 * MARGIN  # 720pt of usable column height
COLUMN = PAGE_WIDTH - 2 * MARGIN  # 540pt of usable width
BULLET_INDENT = 7.0  # body-indent on `set list` in the template
BODY_SIZE = 10.0

# --- Vertical constants, measured across ~500 line transitions in resumes/*.pdf ---

LINE = 13.0  # baseline-to-baseline, any body line
SECTION_COST = 21.2  # a `## ` heading, its rule, and the gap beneath
HEADER_BLOCK = 63.0  # name and contact line, above the first section heading

# Shortfall thresholds, in rendered lines. Set against the model's own resolution:
# calibration residuals run to about 3 lines on the worst case, so a threshold below
# that fires on noise. These are not tuned to catch a draft one line short, which is
# not the failure mode. The drafts this exists to stop come in at half to two thirds of
# a page, 15 to 25 lines short, and clear these by an order of magnitude.
WARN_LINES = 2.0
FAIL_LINES = 4.0

# What --calibrate treats as drift rather than as the known baseline error. Set above
# the worst residual on the calibration set, so it fires when the template has changed
# and the model no longer fits, not on the error the model is already known to carry.
DRIFT_LINES = 4.0

# Helvetica advance widths, units per 1000 em. The template's font stack is
# ("Helvetica", "Arial"), whose metrics are identical for this purpose.
_WIDTHS = {c: 556 for c in "0123456789"}
_WIDTHS.update(
    zip(
        " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~",
        # fmt: off
        [278, 278, 355, 556, 556, 889, 667, 191, 333, 333, 389, 584, 278, 333,
         278, 278, 278, 278, 584, 584, 584, 556, 1015, 278, 278, 278, 469, 556,
         333, 334, 260, 334, 584],
        # fmt: on
    )
)
_WIDTHS.update(
    zip(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        # fmt: off
        [667, 667, 722, 722, 667, 611, 778, 722, 278, 500, 667, 556, 833, 722,
         778, 667, 778, 722, 667, 611, 722, 667, 944, 667, 667, 611],
        # fmt: on
    )
)
_WIDTHS.update(
    zip(
        "abcdefghijklmnopqrstuvwxyz",
        # fmt: off
        [556, 556, 500, 556, 556, 278, 556, 556, 222, 222, 500, 222, 833, 556,
         556, 556, 556, 333, 500, 278, 556, 500, 722, 500, 500, 500],
        # fmt: on
    )
)
_DEFAULT_WIDTH = 556  # em dash, bullet glyph, anything outside Latin-1

SKILLS_LINE = re.compile(r"^\*\*[^*]+:\*\*")
ENTRY_LINE = re.compile(r"^\*\*[^*]+\*\*")


def text_width(text, size=BODY_SIZE):
    """Rendered width of a string in points."""
    return sum(_WIDTHS.get(c, _DEFAULT_WIDTH) for c in text) / 1000.0 * size


def strip_markup(text):
    """Drop markdown emphasis markers, which cost no width when rendered."""
    return text.replace("**", "")


def wrapped(text, available=COLUMN):
    """Rendered line count for one logical line of body text."""
    return max(1, math.ceil(text_width(strip_markup(text)) / available))


def entry_lines(line):
    """Rendered line count for an entry header.

    `entry()` emits a second line only when given both a title and a location, which in
    markdown is the `**Org** - Title | Location | Dates` form. A project header
    (`**Name** - tech | dates`, one pipe) and a bare org-and-location header both
    collapse to one line. Getting this wrong costs three lines on a resume with several
    projects, which is the size of the shortfall being measured.
    """
    if " — " in line and line.count("|") >= 2:
        return 2
    return wrapped(line)


def parse(md):
    """Classify every content line of a draft.

    Returns (elements, bullets), where elements is a list of (kind, rendered_lines).
    """
    elements = []
    bullets = 0
    seen_section = False

    for raw in md.split("\n"):
        line = raw.rstrip()
        if not line.strip():
            continue

        if line.startswith("# "):
            continue  # name, folded into HEADER_BLOCK

        if line.startswith("## "):
            elements.append(("section", 1))
            seen_section = True
            continue

        if not seen_section:
            continue  # contact line, folded into HEADER_BLOCK

        if line.startswith("- "):
            bullets += 1
            elements.append(("bullet", wrapped(line[2:], COLUMN - BULLET_INDENT)))
        elif SKILLS_LINE.match(line):
            elements.append(("plain", wrapped(line)))
        elif ENTRY_LINE.match(line):
            elements.append(("entry", entry_lines(line)))
        else:
            elements.append(("plain", wrapped(line)))

    return elements, bullets


def height(elements):
    """Predicted height of the rendered content block, in points."""
    body = sum(n for kind, n in elements if kind != "section")
    sections = sum(1 for kind, _ in elements if kind == "section")
    return HEADER_BLOCK + body * LINE + sections * SECTION_COST


def report(path):
    elements, bullets = parse(Path(path).read_text(encoding="utf-8"))
    predicted = height(elements)
    short_by = (TEXT_BLOCK - predicted) / LINE
    body_lines = sum(n for kind, n in elements if kind != "section")

    print(f"{path}")
    print(f"  bullets         {bullets}")
    print(f"  rendered lines  {body_lines}")
    print(f"  predicted fill  {predicted / TEXT_BLOCK * 100:.0f}% of the text block")

    if short_by < -1.0:
        print(f"  LONG by ~{-short_by:.1f} lines.")
        print("  Tighten bullets before cutting content. format-rules.md §Page budget.")
        return 1

    if short_by > FAIL_LINES:
        # Bullets run a little over two lines each here, so the shortfall in bullets is
        # roughly the shortfall in lines halved. Reported in bullets because that is the
        # unit being written.
        print(f"  SHORT by ~{short_by:.1f} lines, about {max(1, round(short_by / 2.2))}")
        print("  more bullets. Pull real evidence back from the records; do not widen")
        print("  margins, shrink the font, or pad a bullet with a clause it does not")
        print("  need. format-rules.md §Page budget.")
        return 1

    if short_by > WARN_LINES:
        print(f"  THIN by ~{short_by:.1f} lines. One more bullet would close it.")
        return 0

    print("  OK: fills the page.")
    return 0


def calibrate():
    """Re-measure the model against every rendered PDF and print residuals.

    Run after changing templates/resume-style.typ. Needs poppler's pdftotext.
    """
    import subprocess

    rows = []
    for pdf in sorted(ROOT.glob("resumes/*/resume.pdf")):
        md = pdf.with_name("resume.md")
        if not md.exists():
            continue
        xml = subprocess.run(
            ["pdftotext", "-bbox", str(pdf), "-"], capture_output=True, text=True
        ).stdout
        tops = [float(m) for m in re.findall(r'yMax="([\d.]+)"', xml)]
        if not tops:
            continue
        elements, _ = parse(md.read_text(encoding="utf-8"))
        rows.append((pdf.parent.name, height(elements), max(tops) - MARGIN))

    if not rows:
        print("No rendered resumes to calibrate against.")
        return 1

    print(f"{'resume':40} {'predicted':>9} {'actual':>8} {'error':>7} {'lines':>6}")
    worst = 0.0
    for name, predicted, actual in rows:
        error = predicted - actual
        worst = max(worst, abs(error))
        print(
            f"{name[:38]:40} {predicted:8.0f}pt {actual:7.0f}pt "
            f"{error:+6.0f}pt {error / LINE:+5.1f}"
        )
    print(f"\nworst absolute error: {worst:.0f}pt ({worst / LINE:.1f} lines)")
    if worst > DRIFT_LINES * LINE:
        print(f"Worse than the {DRIFT_LINES:.0f}-line baseline. Refit the constants.")
        return 1
    return 0


def main():
    args = sys.argv[1:]
    if args == ["--calibrate"]:
        return calibrate()
    if not args:
        print("usage: estimate-fill.py <resume.md> [...]   |   --calibrate")
        return 2
    return max(report(path) for path in args)


if __name__ == "__main__":
    sys.exit(main())
