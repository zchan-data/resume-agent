# Render

Turning an approved `resume.md` into a verified PDF.

Only run this after the user has approved the draft.

## Pipeline

```
resume.md     approved content (source of truth)
   |
resume.typ    generated: imports the shared style module, contains only content
   |
resume.pdf    compiled artifact
```

Styling lives in `templates/resume-style.typ` as a set of helper functions. The
generated `resume.typ` imports it and contains content only. This means a styling change
applies to every resume, and the generated file stays short enough to read at a glance.

## Writing resume.typ

Start from `templates/resume-style.typ` — read it to see the available helpers and their
exact signatures. The generated file's shape:

```typst
#import "../../templates/resume-style.typ": *

#show: resume

#header(
  name: "Jordan Rivera",
  contact: (
    "jordan.rivera@example.com",
    "415-555-0142",
    "github.com/jrivera",
    "Oakland, CA",
  ),
)

== Skills

#skills((
  "Languages": "Python, Go, TypeScript, SQL",
  "Frameworks": "React, FastAPI, Node.js",
))

== Experience

#entry(
  org: "Stripe",
  title: "Software Engineer Intern",
  location: "San Francisco, CA",
  dates: "06/2025 - 08/2025",
)
- Cut product catalog API latency from 800ms to 95ms by profiling 14 slow queries
  with pg_stat_statements and eliminating N+1 access patterns.
- Second bullet.

== Projects

#entry(
  org: "Transit Delay Prediction Pipeline",
  title: "Python, XGBoost, scikit-learn, pandas",
  location: "",
  dates: "01/2025 - 04/2025",
)
- Built an end-to-end ML pipeline over 4 seasons of scraped schedule and weather data.
```

Project entries put the tech stack in `title`, not `Personal` or a course/org name — see
`writing-rules.md`'s Projects section. `location` is empty for personal projects.

The relative import path is `../../templates/resume-style.typ` from inside
`resumes/<slug>/`.

### Escaping

Typst treats these as markup in content: `#`, `*`, `_`, `@`, `<`, `>`, `$`, `\`, `~`.

- In string literals (contact entries, `entry()` arguments): escape `\` and `"`.
- In body content (bullets): escape a literal `#` as `\#`, and `@` as `\@`. A bare `@`
  starts a citation and will fail to compile.
- **`~` is a non-breaking space, not a tilde. Escape it as `\~`.** This is the dangerous
  one, because unlike `@` it compiles cleanly and fails silently: `~9x` renders as `9x`,
  which turns "approximately 9x" into an exact claim the record does not support. Any
  approximation carried over from a record (`~9x`, `~3.2 cm`, `~40k requests/day`) hits
  this. Grep the generated `.typ` for a bare `~` before compiling, and confirm the
  tildes survive extraction:
  `pdftotext -layout resume.pdf - | grep -o '~[0-9.]*'`
- `C++`, `C#`, and `.NET` appear frequently in skills — write `C\#` in body content.
  Inside a string literal, `C#` is fine as-is.

Underscores inside identifiers like `pg_stat_statements` are safe in Typst — unlike
LaTeX, no escaping is needed.

## Compiling

Run from the project root. `--root` is required — Typst sandboxes to the input file's
directory by default, and the import of `templates/resume-style.typ` reaches above
`resumes/<slug>/`, which fails with "would escape the project root" without it.

```bash
typst compile --root . resumes/<slug>/resume.typ resumes/<slug>/resume.pdf
```

To eyeball the layout before showing the user, render a PNG to the scratchpad and read
it:

```bash
typst compile --root . --format png --ppi 110 resumes/<slug>/resume.typ /tmp/preview.png
```

Compile errors report a line number in `resume.typ`. Fix the `.typ`, not the `.md` —
the markdown is the user's approved content and must stay in sync with what they saw.

If a fix changes content rather than markup, say so and get approval.

## Verification

Two checks, both required. A PDF that looks correct but extracts incorrectly is the
exact failure this system exists to prevent, and it is invisible without checking.

### 1. Page count

```bash
pdfinfo resumes/<slug>/resume.pdf | grep -E 'Pages|Page size'
```

Use `pdfinfo`, not `mdls` — `mdls` reads the Spotlight index and returns `(null)` for a
file written seconds ago, which looks like a failure but is just a stale index.

Must be 1 unless the two-page exception in `format-rules.md` applies. If it spilled,
tighten bullets — do not shrink the font below 10pt or the margins below 0.5in.

### 2. Text extraction order

`pdftotext` (from poppler, already installed) simulates what a parser sees. Run both
modes — they exercise different extraction strategies and can disagree.

```bash
# position-aware, what most modern ATS do
pdftotext -layout resumes/<slug>/resume.pdf -

# raw stream order, what a naive sequential parser does
pdftotext resumes/<slug>/resume.pdf -
```

Confirm in both:

- Name and every contact field present and intact
- Section headings appear as the literal strings `Skills`, `Education`, `Experience`,
  `Projects`
- Each entry's organization and title read together, not interleaved with another entry
- Bullets appear in order, none merged or dropped
- No stray glyphs. Only `•` should be non-ASCII:
  `pdftotext resume.pdf - | LC_ALL=C grep -o '[^ -~]' | sort -u`
- Every approximation sign that was in the draft is still in the PDF. A missing `~`
  silently upgrades an estimate into an exact figure, which is a truthfulness defect
  rather than a formatting one. See §Escaping.

**Known and accepted:** in raw stream mode, right-aligned dates and locations are
emitted after their entry's bullets rather than beside the organization, because the
wide whitespace gap reads to a naive extractor as a column boundary. Position-aware
mode places them correctly. This is the documented tradeoff behind `LINEAR_DATES` in
`templates/resume-style.typ` — right alignment serves the recruiter's right-margin date
scan, which is worth more than the residual risk. Flip `LINEAR_DATES` to `true` for a
known-strict parser (Workday, Taleo) to get strictly linear output at the cost of that
scan.

Anything else scrambled is a genuine defect. The cause is almost always a layout
construct that positions text absolutely — `resume-style.typ` avoids grids and tables
specifically for this reason. Do not introduce them into a generated file.

## Reporting back

Tell the user the output path, the page count, and confirm extraction verified. If
anything was tightened to fit one page, say what.
