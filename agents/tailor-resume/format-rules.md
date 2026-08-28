# Format Rules

Layout, section order, and the ATS constraints that govern everything rendered.

## The two readers

**The parser** strips all formatting and tries to map remaining text into database
fields. It reads top-to-bottom, left-to-right. Anything that disrupts that linear order
corrupts the extracted record — and a corrupted record is an automatic rejection the
user never learns about.

**The human** spends about seven seconds, scanning in an F-pattern: a pass across the
top third, a skim down the left margin for headers and titles, occasional saccades right
to check dates. Roughly 80% of attention lands in the top third of page one.

Every rule below serves one or both.

## Non-negotiable ATS rules

**Single column, always.** Two-column layouts are the leading cause of parser failure.
Because parsers extract horizontally, a narrow skills rail beside a wide experience
column gets interleaved line by line into unreadable output. This is not a marginal
risk — on the strictest parsers it fails outright.

**Standard section headings, literally spelled.** Parsers map sections by exact string
match. Use:

- `Education`
- `Skills` or `Technical Skills`
- `Experience` or `Work Experience`
- `Projects`

Never invent alternatives. "My Journey", "Toolkit", "What I Bring" cause the entire
section to be dropped — the work disappears from the database completely.

**No tables, no text boxes.** Table cells are read in raw markup order, which scrambles
dates against titles. Text box content is often treated as a separate layer and ignored
entirely. Use whitespace-based alignment instead.

**No graphics, icons, or images.** Parsers strip them. An envelope glyph instead of the
word "Email" means the contact field is lost, leaving no automated way to reach the
candidate.

**No headers or footers.** Some parsers drop them wholesale. Contact information in a
header is the most common way applicants lose their own phone number. Put contact
details in the document body.

**Consistent `MM/YYYY` dates everywhere.** Parsers compute total years of experience
from these and filter on the result. Mixed formats break the calculation.

**Standard fonts only.** Helvetica, Arial, Calibri, Georgia, Garamond, Times New Roman.
Anything exotic risks character substitution during extraction. The Typst template pins
Helvetica with fallbacks.

**No photo.** In the US it is a straightforward negative: it consumes a large share of a
seven-second scan on a face rather than qualifications, and introduces bias the
candidate cannot control.

## Page budget

**One page.** Hard limit for students, new grads, and anyone under roughly ten years of
experience. Two pages only for an advanced degree with publications, or a genuinely long
senior career.

At 10pt with 0.5in margins, one page is about 40–45 content lines. Approximate
allocation for a new grad:

| Section | Lines |
| --- | --- |
| Contact header | 3 |
| Skills | 4–5 |
| Education | 3–4 |
| Experience | 16–22 |
| Projects | 8–12 |

Running long: tighten bullets to one line before cutting content. Most two-line bullets
have a redundant clause.

Running short: this is a real signal, not a formatting problem. Add depth from the
records rather than padding margins and font size. If genuinely short on material, say
so and offer to capture more experience.

## Section order

### New grad and student (default)

```
Contact header
Skills
Education          <- honors, GPA if >= 3.5, relevant coursework
Experience         <- internships, part-time, research
Projects           <- treated as real experience
```

Education sits high because it is the strongest credential available and because the
research on institutional guidance is explicit that recent graduates should lead with
it. Skills sit above it so the top third carries keyword density for both readers.

### Mid-level and above

```
Contact header
Summary            <- max 4 lines
Skills
Experience         <- dominates the top third
Projects           <- trimmed or cut entirely
Education          <- bottom, no graduation year
```

### Switching between them

Move to the mid-level layout when the user has roughly two or more years of full-time
professional experience after graduating. Read `profile/identity.md` for the current
stage. When in doubt near the boundary, ask.

The trigger is full-time professional experience, not age or total internships.

## Contact header

Name on its own line, largest text on the page. Then one line of contact details
separated by a plain delimiter:

```
Jordan Rivera
jordan.rivera@example.com | 415-555-0142 | github.com/jrivera | linkedin.com/in/jrivera | Oakland, CA
```

- Use the literal words or plain URLs, never icons
- City and state only — no street address
- Include GitHub for any engineering role; it is direct external validation of claims
- Personal domain email is fine, Gmail is fine. Avoid AOL, Hotmail, and Yahoo — for a
  technology employer they read as out of touch, at no benefit
- **If the user is outside the job's location, state relocation intent explicitly**
  (`Relocating to Seattle, 06/2026` or `Open to relocation`). Recruiters reject
  out-of-area candidates by default rather than open a negotiation; one phrase prevents
  it

## Whitespace and typography

Dense text triggers immediate negative bias — a wall of text is discarded before it is
read. Protect white space:

- 10pt minimum body text; 10–11pt is the working range
- 0.5in minimum margins
- Section headings in bold, visually distinct enough to anchor the left-margin skim

**Vertical rhythm must be strictly ordered.** The reader infers structure from *relative*
gap size, not absolute size. Every gap must exceed the gap one level below it:

```
section  >  entry  >  between bullets  >  entry-header-to-bullets  >=  line leading
```

Any inversion makes two units merge visually. Three real inversions have been found in
this template, all by eye and none by any automated check:

| Inversion | Symptom |
| --- | --- |
| entry gap < bullet gap | consecutive jobs merge into one block |
| bullet gap < line leading | one wrapped bullet reads as two separate bullets |
| 19pt name spaced by 10pt `par.leading` | name's descenders crowd the contact line |

The third was structural rather than a wrong value: the name and contact line were joined
by `linebreak()` inside one paragraph, so their separation came from `par.leading`, sized
for body text. **Elements at different type sizes must be separate blocks**, each with
explicit spacing — never lines of a shared paragraph.

This is not cosmetic. Dense text without clear white space triggers immediate negative
bias, and the F-pattern skim down the left margin needs visible boundaries to lock onto.

The values live as named constants at the top of `templates/resume-style.typ`
(`SPACE_SECTION`, `SPACE_ENTRY`, `SPACE_BULLET`, `SPACE_ENTRY_BODY`, `LEADING`). Adjust
them there, never inline, and preserve the ordering.

**When checking a rendered PDF, look at it as an image, not only as extracted text.**
Extraction verifies the parser's view; only the rendered page reveals whether a human can
tell where one entry stops and the next begins. Both checks are required.

A thin horizontal rule under section headings materially aids the F-pattern scan and is
a drawn object that does not affect text extraction. Some institutional guidance advises
against rules entirely; the template makes this a one-line toggle. It is on by default.

Avoid italics for anything load-bearing. The template uses bold for organizations and
regular weight for titles, which reads cleanly and avoids the question.

## Never do

- Hide keywords in white text or set them to 1pt. Parsers surface hidden text and
  present it to the recruiter as plain visible text, which reads as attempted deception
  and disqualifies immediately.
- Stuff keywords the user cannot support. It dilutes genuine expertise and fails on
  human review when the skills list is not corroborated by the experience section.
- Include references, "References available upon request", objectives, or personal
  details like age, marital status, or nationality.
