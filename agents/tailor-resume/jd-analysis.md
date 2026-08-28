# Job Description Analysis

Convert prose into an explicit, checkable specification before writing anything.

## Why this step exists

A job description is a requirements document written by someone who was not trying to
write a requirements document. Requirements are scattered, duplicated, buried in
paragraphs about company culture, and stated at wildly different levels of importance.

Extracting them explicitly is what makes tailoring real. Without this step you end up
lightly rewording a generic resume and calling it tailored.

## Output

Two files, with different readers.

**`match-analysis.md` is read by machines.** The cover letter agent reloads it in full,
and you reload it on every re-run. Everything in it is a table or a short list. Target
90 lines; treat 120 as a hard ceiling. Nothing in it explains itself.

**`analysis-notes.md` is read by the user.** Reasoning, judgment calls, gap strategy,
anything you would say out loud to justify a decision. No agent ever loads this file, so
length here is free.

The split matters because these two costs are not alike. `match-analysis.md` is written
once and re-read many times, by an agent that pays for every token of it. Prose that
belongs to the reasoning, not the decision, is charged to every later step for no gain.

The rule for placing a sentence: **if an agent would act differently without it, it goes
in `match-analysis.md`.** Otherwise it goes in the notes. A requirement, a keyword, a
score, a prohibition changes behavior. Why the score felt right does not.

One deliberate exception, below.

## Procedure

### 1. Classify the role

One line each. The reasoning behind a call goes in `analysis-notes.md`.

- **Domain** — backend, frontend, ML, infra, data, product. Use the vocabulary from the
  `domains` list in `add-experience/record-schema.md` so it matches record tags.
- **Seniority** — intern, new grad, junior, mid, senior, staff. Read the years-of-
  experience line, but weight the *responsibilities* more heavily; postings inflate
  years routinely.
- **Company shape** — early startup, growth, big tech, non-tech enterprise, agency.
  This shifts emphasis: startups reward breadth and shipping speed, enterprises reward
  scale and process, big tech rewards depth and systems.

### 2. Extract requirements into three tiers

| Tier | How to spot it | Weight |
| --- | --- | --- |
| **Hard** | "required", "must have", "N+ years of X", listed first, repeated | Must evidence if at all possible |
| **Preferred** | "nice to have", "bonus", "plus", "familiarity with" | Evidence if cheap |
| **Implied** | Not stated but obvious from the role and stack | Evidence opportunistically |

Repetition is the strongest signal available. If a technology appears in the summary,
the responsibilities, and the qualifications, it is the job. Rank it first regardless of
which tier its phrasing suggests.

Record each requirement as a checkable statement, not a copied phrase. "Experience
building REST APIs in a compiled language" rather than "3+ years backend experience".

### 3. Extract literal keywords

ATS platforms are literal string matchers. Semantic understanding is limited and
inconsistent across vendors. If the posting says "Product Manager" and the resume says
"PM", a search for the former may not surface the candidate.

Build a keyword list capturing:

- **Exact technology strings** as the posting writes them — `PostgreSQL` not `Postgres`,
  `Node.js` not `Node`, `CI/CD` not `continuous integration`
- **Acronym-and-expansion pairs** where both forms plausibly appear in a recruiter
  search: write `Continuous Integration/Continuous Deployment (CI/CD)` once, naturally,
  and the resume satisfies either query
- **Role and methodology nouns** — `distributed systems`, `microservices`, `Agile`,
  `code review`, `on-call`
- **Verb phrases the posting uses** for the actual work — `design and implement`,
  `debug production issues`, `partner with product`

Mark each keyword: do the records support it, or not? A keyword with no backing evidence
does not go on the resume. That is keyword stuffing, and it fails twice — modern
platforms detect it, and a human reading a skills list that the experience section does
not corroborate discounts the whole document.

### 4. Note disqualifiers and logistics

Things that get an application dropped regardless of technical fit:

- Work authorization or clearance requirements
- Location, and whether onsite/hybrid/remote — if the user is out of area, the resume
  must state relocation intent explicitly or recruiters reject rather than negotiate
- Degree requirements
- Hard years-of-experience floors

Flag these to the user. Some are fatal and worth knowing before spending effort.

### 5. Identify what the role actually optimizes for

**This is the deliberate exception: prose, and it stays in `match-analysis.md`.**

Two to four sentences, in your own words: what does this team need this person to *do*?
An SRE posting heavy on incident response wants someone who has been paged at 3am. A
platform posting wants someone who has built for other engineers. This judgment drives
which accomplishments lead — a correct read here is worth more than perfect keyword
coverage.

It earns its place because two later steps consume it directly and neither can recover
it from the tables: `selection-rules.md` §3 uses it to break ties on coverage, and
`../write-cover-letter/story-selection.md` §1 calls it more important than the
requirement table for choosing what the letter argues. Demoting it to the notes would
mean the letter agent reloads the whole job description to reconstruct it, which costs
far more than the paragraph.

Keep it to four sentences. Supporting evidence for the read goes in the notes.

## Templates

### `match-analysis.md`

Every cell is a phrase, not a sentence. `Strength` is one of `strong`, `moderate`,
`thin`, `none`, optionally with a two-or-three-word qualifier (`strong, single-source`).
Anything longer belongs in the notes.

```markdown
# Match Analysis — <Company> / <Role>

## Role classification
- Domain:
- Seniority:
- Company shape:

**What this role actually optimizes for:** <2-4 sentences. The one prose block that
stays in this file.>

## Requirements

### Hard
| # | Requirement | Evidence | Strength |
|---|---|---|---|
| H1 | | | |

### Preferred
| # | Requirement | Evidence | Strength |
|---|---|---|---|
| P1 | | | |

### Implied
| # | Requirement | Evidence | Strength |
|---|---|---|---|
| I1 | | | |

## Keywords
| Keyword (literal) | Supported by | Placement |
|---|---|---|

## Do not use
<!-- One line each: the string, then the reason in a clause. -->
- `<keyword>` — <reason>

## Logistics and disqualifiers
<!-- One line each. Fatal items first. -->
-
```

`selection-rules.md` §6 appends `## Selected`, `## Cut`, and `## Gaps` in the next step.

### `analysis-notes.md`

```markdown
# Analysis notes — <Company> / <Role>

Reasoning behind `match-analysis.md`. Written for the user. No agent reads this file.

## How the requirements were read
<!-- Repetition ranking, what the posting emphasizes, anything ambiguous. -->

## Selection judgment calls
<!-- Deliberate departures from the scoring, and why. -->

## Gaps, and what to do about them
<!-- The full strategy per unevidenced requirement: whether to address it in the cover
     letter, build something first, or run add-experience. This is the section the user
     actually acts on, and it is the one that used to bloat match-analysis.md. -->

## Logistics detail
<!-- Term length, on-site expectations, anything the user should weigh before applying. -->
```

Leave `Evidence` and `Strength` empty at this stage — `selection-rules.md` fills them in
the next step. Extracting requirements before looking at the user's history keeps the
analysis honest; doing both at once biases the extraction toward what you already know
the user has.
