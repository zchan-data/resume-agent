# Format Rules

Length, layout, keywords, and the shape of the draft file.

## The two readers, reweighted

The resume serves a parser first and a human second. The cover letter inverts that.

The parser still runs, and the letter still has to survive it, so the ATS constraints below
are non-negotiable. But nobody is hired because their cover letter had good keyword
density. The letter's value is entirely in what a person thinks after reading it, which is
why `voice-rules.md` outranks this file whenever the two pull against each other.

## Length

- **One page. Always.** No exceptions at any seniority.
- **250 to 350 words.** Hard cap 400.
- **Three or four paragraphs.** Pain Letter format runs shorter, often under 250.

Under-length is not a problem. A tight 260-word letter that says two real things reads as
respect for the reader's time. Padding to fill a page is visible and it is the first place
generic sentences get added.

Over-length is a problem, and the fix is never smaller type. Cut the weakest evidence
entirely rather than compressing everything uniformly.

## Document structure

```
Jordan Rivera
jordan.rivera@example.com | 415-555-0142 | github.com/jrivera | Oakland, CA

August 20, 2026

Hiring Team, Operations
Northwind Robotics

Dear Northwind Robotics Operations Team,

<body paragraphs>

Sincerely,
Jordan Rivera
```

Details:

- **Contact block in the document body, never in a page header.** Some parsers drop
  headers and footers wholesale, which is the most common way an applicant loses their own
  phone number.
- **Match the resume's contact line exactly**, same fields in the same order, so the two
  documents read as one packet.
- **Date written out** (`August 20, 2026`). This is the one place in the system that does
  not use `MM/YYYY`; a letter with a numeric dateline reads as a generated document.
- **Recipient block is optional** and only worth including when you have a real name or a
  real team from `company-research.md`. A recipient block addressed to nobody in
  particular is worse than none.
- **Salutation**: name if verified, team if not, `Dear Hiring Manager` as the fallback.
  Never `To Whom It May Concern`.
- **Sign off** with `Sincerely,` and the name. `Best,` and `Thanks,` are both fine.
  Anything more elaborate is not.

## ATS constraints

The letter is uploaded and parsed alongside the resume. Everything structural that
scrambles a resume scrambles a letter.

- **Single column.** No side panels, no split layouts.
- **No tables.** A real table, in HTML, Word, or Typst, is read by an ATS in raw cell
  order and produces a scrambled or empty record. There is no layout a letter needs badly
  enough to risk that.
- **No images, icons, logos, or graphical letterhead.** Parsers strip them, and an
  envelope glyph in place of the word "Email" loses the contact field entirely.
- **No headers or footers.**
- **Standard fonts.** Helvetica, Arial, Calibri, Georgia, Garamond, Times New Roman. The
  Typst template pins the same stack as the resume.
- **Selectable text.** Never export a flattened or image-based PDF.

## Keywords

The letter should hit roughly 60 to 80% of the job description's critical keywords,
naturally, inside real sentences.

Working method:

1. Take the keyword table from `match-analysis.md`. It is already built and already marked
   for which keywords the records support.
2. Use only supported keywords. An unsupported keyword in a letter is worse than on a
   resume, because prose implies a claim of experience rather than a list entry.
3. Use the posting's exact strings. `PostgreSQL` not `Postgres`, `React.js` not
   `JavaScript frameworks`, `AWS EC2` not `cloud infrastructure`. Recruiters run literal
   Boolean searches against the ATS database, and the exact form is what surfaces.
4. Weave them into the accomplishment, never into a list. "Built a Python extraction
   pipeline over Google Cloud Document AI" carries the keywords and proves application at
   once.

**Do not aim for 100%.** Modern platforms detect stuffing with NLP, and a human reading a
letter that recites the requirements back verbatim discounts the entire document. If the
letter's natural content misses a keyword, let it miss. The resume carries the coverage
load; the letter is a secondary surface for it.

Never hide keywords in white text or 1pt type. Parsers surface hidden text and present it
to the recruiter as ordinary visible text, which reads as attempted deception and
disqualifies immediately.

## Submission format

- **PDF by default.** Greenhouse, Lever, and Ashby handle single-column PDFs well.
- **Plain text when the portal gives you a textarea.** Many applications paste the letter
  into a form field rather than accepting an upload. In that case strip every markdown
  artifact: no `**`, no `#`, no bullet characters that will not survive a copy-paste.
  Offer the user a plain-text version when the application URL suggests a paste box.
- **DOCX for Workday and Taleo.** Not yet implemented, same deferred item as the resume
  agent. Flag it to the user when the application URL is a `myworkdayjobs.com` or Taleo
  instance so they know the PDF is a compromise rather than a choice.

## Typography

Handled by `templates/cover-letter-style.typ`. The values, and why:

- 10.5pt body, 1in margins. A letter is short, so it can afford whitespace the resume
  cannot, and dense text triggers immediate negative bias.
- Ragged right, never justified. Justification produces uneven word spacing and reads as a
  template.
- Paragraph spacing rather than first-line indents. Modern business letter convention, and
  it survives text extraction more cleanly.
- Same font stack as the resume, so the packet looks coherent.

## The draft file

Write `cover-letter.md` in the application folder, with frontmatter recording the
decisions so a re-run does not have to reconstruct them:

```markdown
---
target: Northwind Robotics / Operations Analyst
format: standard narrative
format_reason: portal application, structured ATS, no verified hiring manager name
addressee: team (no name verified)
magnified: exp-acme-2026/ACC-001 (lead), exp-northlake-athletics-2024/ACC-002 (support)
company_facts: C1, C3 from company-research.md
imperfect_moment: hand-replaying a month of source files before the pattern appeared (ACC-001 context)
word_count: 312
submission: PDF
---
```

Then the letter itself, in the document structure above, as plain prose. The markdown file
is what the user approves and what the Typst file is generated from, so it must contain the
exact words that will appear in the PDF.
