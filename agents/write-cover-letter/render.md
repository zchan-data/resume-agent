# Render

Turning an approved `cover-letter.md` into a verified PDF.

Only run this after the user has approved the draft.

## Pipeline

```
cover-letter.md     approved content (source of truth)
   |
cover-letter.typ    generated: imports the shared style module, contains only content
   |
cover-letter.pdf    compiled artifact
```

Same arrangement as the resume. Styling lives in `templates/cover-letter-style.typ`; the
generated file holds content only, so a styling change applies to every letter and the
generated file stays short enough to read at a glance.

The words in the PDF must be the words the user approved. If a compile fix would change
content rather than markup, stop and ask.

## Writing cover-letter.typ

Read `templates/cover-letter-style.typ` for the available helpers and their exact
signatures. The shape:

```typst
#import "../../templates/cover-letter-style.typ": *

#show: letter

#letterhead(
  name: "Jordan Rivera",
  contact: (
    "jordan.rivera@example.com",
    "415-555-0142",
    "github.com/jrivera",
    "Oakland, CA",
  ),
)

#dateline("August 20, 2026")

#recipient(lines: ("Hiring Team, Operations", "Northwind Robotics"))

#salutation("Dear Northwind Robotics Operations Team,")

First body paragraph.

Second body paragraph.

#signoff(name: "Jordan Rivera")
```

The relative import path is `../../templates/cover-letter-style.typ` from inside
`resumes/<slug>/`.

Body paragraphs are plain Typst paragraphs separated by a blank line. Do not wrap them in
blocks, and do not add manual `#v()` spacing. The template owns the vertical rhythm, and
inline spacing overrides are how that rhythm gets broken one letter at a time.

Omit `#recipient` entirely when there is no verified name or team.

### Escaping

Typst treats these as markup in content: `#`, `*`, `_`, `@`, `<`, `>`, `$`, `\`.

- In string literals (contact entries, `dateline`, `salutation`, `recipient` lines):
  escape `\` and `"`.
- In body content: escape a literal `#` as `\#` and `@` as `\@`. A bare `@` starts a
  citation and fails to compile, which matters here because email addresses appear in
  prose more often in a letter than on a resume.
- `C++`, `C#`, and `.NET`: write `C\#` in body content. Inside a string literal, `C#` is
  fine as-is.

Underscores inside identifiers like `pg_stat_statements` are safe in Typst.

## Compiling

Run from the project root. `--root` is required, because the import reaches above
`resumes/<slug>/` and Typst otherwise sandboxes to the input file's directory.

```bash
typst compile --root . resumes/<slug>/cover-letter.typ resumes/<slug>/cover-letter.pdf
```

To eyeball the layout before showing the user:

```bash
typst compile --root . --format png --ppi 110 \
  resumes/<slug>/cover-letter.typ /tmp/cl-preview.png
```

Compile errors report a line number in `cover-letter.typ`. Fix the `.typ`, never the
`.md`.

## Verification

Three checks. All required.

### 1. Page count

```bash
pdfinfo resumes/<slug>/cover-letter.pdf | grep -E 'Pages|Page size'
```

Must be 1. There is no two-page exception for a cover letter at any seniority. If it
spilled, cut a sentence. Do not shrink the type or the margins.

Use `pdfinfo`, not `mdls`: `mdls` reads the Spotlight index and returns `(null)` for a
file written seconds ago.

### 2. Text extraction

```bash
# position-aware, what most modern ATS do
pdftotext -layout resumes/<slug>/cover-letter.pdf -

# raw stream order, what a naive sequential parser does
pdftotext resumes/<slug>/cover-letter.pdf -
```

Confirm in both:

- Name and every contact field present and intact
- The letter reads in order: letterhead, date, recipient, salutation, body, sign-off
- No paragraph merged into another or dropped
- No stray glyphs. Only the pipe delimiter and ASCII should appear:
  `pdftotext resumes/<slug>/cover-letter.pdf - | LC_ALL=C grep -o '[^ -~]' | sort -u`

The letter has no right-aligned content, so unlike the resume both extraction modes
should produce the same reading order. Compare word order, not lines:

```bash
diff <(pdftotext -layout resumes/<slug>/cover-letter.pdf - | tr -s '[:space:]' '\n') \
     <(pdftotext resumes/<slug>/cover-letter.pdf - | tr -s '[:space:]' '\n')
```

A line-for-line diff always reports differences and they are meaningless: `-layout` emits
blank lines between blocks and wraps to the visual line, raw mode does neither. Only a
difference in **word sequence** is a defect, and unlike the resume's right-aligned dates
there is no documented exception here, so any real divergence needs investigating.

### 3. Look at the rendered page

Extraction verifies the parser's view and reveals nothing about whether the page reads
well. Render the PNG and read it as an image.

Check specifically:

- Paragraph gaps are visibly larger than the gaps between wrapped lines inside a
  paragraph. When those two converge, a new paragraph reads as a continuation of the last
  one, and the letter turns into a wall.
- Nothing collides. A tight `#v()` value can overlap two lines in a way that extracts
  perfectly and looks broken, so extraction passing is not evidence the page is fine.
- The page is not bottom-heavy or stranded. Under 300 words on a letter-size page leaves
  a large white area below the signature. That is normal and correct, and it is not a
  reason to pad.

## Plain-text variant

Many portals paste the letter into a form field instead of accepting an upload. When the
application URL suggests a textarea, also give the user the plain-text body: no markdown
syntax, no bold markers, straight quotes, blank line between paragraphs.

Offer it rather than waiting to be asked. Pasting markdown into a form field puts literal
asterisks in front of the hiring manager.

## Reporting back

Give the user the output path, the page count, the word count, and confirmation that
extraction verified. If you cut anything to fit one page, say what.
