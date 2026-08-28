---
name: write-cover-letter
description: Turn a job description into a tailored, human-sounding cover letter or cold outreach email, built from captured experience records and sourced company research. Use when the user asks for a cover letter, a letter of interest, or a message to a hiring manager or recruiter for a specific role.
---

# Write Cover Letter

A resume is a database record. A cover letter is a piece of writing, and it is read as
one.

That difference drives everything here. The resume agent optimizes for a parser and a
seven-second scan. This agent optimizes for a person who is tired, has read forty
applications today, and can recognize machine-generated prose on sight. Roughly 74% of
recruiters say they can spot an AI-written application, and about 80% of hiring managers
hold it against the candidate. A polished, generic letter is worse than no letter,
because it costs the reader time and returns nothing.

So the job is not "write a good letter." It is: prove specific human effort, on this
company, from this candidate, in prose that could not have been produced by pasting a
job description into a model.

## Hard constraints

- **Read only from `experiences/`, `profile/`, and the application folder. Write only
  into `resumes/<application-slug>/`.** Never modify an experience record.
- **Never invent a fact about the user.** Same invariant as everywhere else in this
  system. No metric, date, title, technology, or outcome that is not in a record.
- **Never invent a fact about the company either.** This is the failure mode specific to
  cover letters. A hallucinated funding round, product name, or engineering blog post is
  an instant rejection, and unlike a soft resume bullet the reader will notice
  immediately because it is their own company. Every company claim traces to a source
  recorded in `company-research.md`.
- **Never contradict the resume.** If `resume.md` exists in the folder, the letter must
  agree with it on every title, date, and number.
- **Stop at the draft.** `cover-letter.md` is an approval gate. Never render a PDF until
  the user has seen the markdown and approved it.
- **The letter is not a prose resume.** It magnifies one or two things. If a sentence
  could be swapped into the resume unchanged, it does not belong here.

## Contract

What each step reads and writes. **Read the named sections, not the whole file** — with
one exception, marked below.

| # | Step | Reads | Writes |
| --- | --- | --- | --- |
| 1 | Locate or create folder | `<app>/match-analysis.md` — `## Role classification`, `## Hard`, `## Keywords`, `## Do not use` only · `resume.md` if it exists · otherwise `../tailor-resume/jd-analysis.md` (all) | `job-description.md`, `match-analysis.md`, `analysis-notes.md` (only if absent) |
| 2 | Research the company | `company-research.md` (all) | `<app>/company-research.md` |
| 3 | Choose the format | `letter-strategy.md` §The two formats, §Weighting by career stage, §Weighting by role type — then only the chosen format's section · or `cold-outreach.md` (all) instead of all of the above | — |
| 4 | Select the material | `story-selection.md` (all) · `## Claims` then `## Narrative` of the records behind the chosen accomplishments | — |
| 5 | Write the draft | `voice-rules.md` (**all — do not section-route this file**) · `format-rules.md` §Length, §Document structure, §ATS constraints, §Keywords, §The draft file | `cover-letter.md` |
| 6 | Audit | `voice-rules.md` §Audit checklist, §Rhythm (in context) | `cover-letter.md` (revised) |
| 7 | Stop and present | — | — |
| 8 | Render | `render.md` (all) · `format-rules.md` §Submission format, §Typography | `cover-letter.typ`, `cover-letter.pdf` |
| 9 | Verify | already in context from step 8 | — |

**`voice-rules.md` is read whole, every time.** System invariant 9 makes it binding for
every prose deliverable, and its failure mode is cumulative: a letter can pass each
individual rule you happened to load and still read as machine-written. Section-routing
it would defeat the one file that most needs to be in context entire.

`format-rules.md` §The two readers, reweighted is absent from step 5 because this file's
opening restates it.

## Procedure

### 1. Locate or create the application folder

Cover letters live in the same folder as the resume for that application:
`resumes/<YYYY-MM-DD>-<company-slug>-<role-slug>/`. One folder per application, holding
the job description, the analysis, the resume, and the letter together. This is
deliberate: the letter has to agree with the resume, and the expensive job-description
analysis is already sitting there.

Three cases:

- **Folder exists with `match-analysis.md`.** Best case. The requirements extraction and
  coverage matrix are already done and still valid. Read `resume.md`, and read the four
  sections of the analysis this agent uses:

  ```bash
  python3 scripts/read-section.py -s "Role classification" -s Hard -s Keywords \
      -s "Do not use" resumes/<slug>/match-analysis.md
  ```

  That is the whole input. `## Selected`, `## Cut`, and `## Gaps` are resume bookkeeping
  and change nothing about the letter. `analysis-notes.md` is written for the user and is
  never read here. `job-description.md` only needs opening if the analysis leaves
  something genuinely unclear — it is the raw material the analysis already reduced.

  If that command errors on a missing section, the folder predates the analysis split and
  holds one long file with `## Unsupported keywords (do not use)` in place of
  `## Do not use`. Read it whole; it is older and larger but complete.

  Skip to step 2.
- **Folder does not exist.** Create it, save the job description verbatim as
  `job-description.md`, then read `../tailor-resume/jd-analysis.md` and follow it to
  produce `match-analysis.md`. You need the requirement tiers and the "what this role
  actually optimizes for" read before you can choose what to magnify.
- **User wants a letter only, no resume.** Fine. Do the analysis anyway. Offer once that
  running tailor-resume afterward is cheap since the analysis is shared, then move on.

### 2. Research the company

Read this agent's `company-research.md` and follow it. Its output is a file of the same
name written into the application folder: `resumes/<slug>/company-research.md`.

Do not skip this and do not do it from memory. Specificity about the company is the
single highest-signal element of the whole letter, and it is the only part a competing
applicant cannot mass-produce. It is also the part most likely to be fabricated if you
work from recall, which is why every claim gets a source line.

### 3. Choose the format

Read `letter-strategy.md` §The two formats, §Weighting by career stage, and §Weighting
by role type. Decide between Standard Narrative, Pain Letter, and cold outreach, and
record the choice with a one-line reason at the top of the draft.

Then read only the section for the format you chose. The format sections are mutually
exclusive and loading both is an avoidable read.

The default is Standard Narrative. The Pain Letter wins in specific, identifiable
situations, and §The two formats says which.

If the user wants a cold email to a hiring manager rather than a portal submission, read
`cold-outreach.md` instead. It is a different document with a different structure, not a
shortened letter.

### 4. Select the material

Read `story-selection.md`. Pick the one or two accomplishments the letter will magnify,
and decide what each one is doing.

This is the step that separates a letter from a summary. A cover letter has room for
roughly two hundred words of evidence. Spending it on breadth reproduces the resume in
worse formatting.

### 5. Write the draft

Write `cover-letter.md`.

Read `voice-rules.md` in full. It is the important one, it is not optional polish, and it
is the one file in this system you do not section-route. Read it before writing the first
sentence, not after producing a draft you then try to repair. A draft written in default
register and humanized afterward reads exactly like what it is.

From `format-rules.md` read §Length, §Document structure, §ATS constraints, §Keywords,
and §The draft file. §Submission format and §Typography are render-time and wait for
step 8.

### 6. Audit the draft against the voice rules

Run `voice-rules.md` §Audit checklist on your own output, including the sentence-length
check in §Rhythm. Both are already in context from step 5. Fix what fails. Do this before
showing the user anything.

Every letter fails something on the first pass. If yours does not, you did not audit it.

### 7. Stop and present

Show the user the draft. Report, concisely:

- The format you chose and why
- Which accomplishments you magnified, and what each is doing in the letter
- Every company claim and where it came from, so the user can sanity-check facts about
  an organization they may know better than your sources do
- Anything you wanted and did not have: an unverifiable hiring manager name, a missing
  metric, a requirement with no evidence
- Anything you deliberately left out

Then wait. Do not render.

Ask the user to read it aloud. It is the fastest test there is, and they will catch
anything that does not sound like them in about thirty seconds.

### 8. Render on approval

Once approved, read `render.md` and produce `cover-letter.typ` and `cover-letter.pdf`.
Read `format-rules.md` §Submission format and §Typography now — they are the parts of
that file deferred from step 5.

If the user hand-edited `cover-letter.md`, render from their version. Never regenerate
the draft from scratch after they have touched it without asking. Their edits are the
most human sentences in the document, by definition.

### 9. Verify the output

Confirm one page, and confirm the PDF's text layer extracts cleanly with the contact
details intact. `render.md` §Verification covers how, and is already in context from
step 8.

## Re-running

If the user comes back wanting changes, do not rebuild. Read the existing
`company-research.md` and `cover-letter.md`, make the targeted edit, re-audit the
paragraphs you touched, and re-render.

A second full pass tends to sand off the specific, slightly awkward phrasing that made
the first draft sound human. Protect it.

## When the evidence is thin

If the records cannot support the role, say so before writing rather than compensating
with enthusiasm. A cover letter is where a weak match becomes obvious, because there is
nothing to write about except the match.

Two honest options, and the user picks:

1. Run the add-experience agent to capture something relevant that was never recorded.
   This is often the real fix, because the gap is usually in the records rather than in
   the user's life.
2. Write the strongest honest letter available, leading on transferable method and
   demonstrated ability to learn, and name the gap to the user so they are not surprised
   in a screen.

Do not write a letter whose central claim the records do not support. Unlike a resume
bullet, the letter's argument is a single continuous thing, and a reader who does not
believe it stops reading.
