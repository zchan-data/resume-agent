# Writing Rules

How to build an individual bullet, and the summary and skills sections.

## The bullet formula

Every experience bullet follows XYZ:

> **Accomplished [X], as measured by [Y], by doing [Z].**

- **X** — the result. What became true that was not true before.
- **Y** — the measurement. Numbers with units and direction.
- **Z** — the method. The specific technology, pattern, or decision.

All three elements must be present. Diagnose a weak bullet by asking which one is
missing:

- No X → it describes a task, not an accomplishment
- No Y → it asserts without evidence
- No Z → it hides what the person actually did, and reads as team credit

Order is flexible. Leading with the metric is often stronger during a seven-second scan
because the number is the highest-contrast token on the line:

> Cut p95 checkout latency from 2.4s to 380ms by replacing synchronous inventory
> lookups with a Redis-backed read-through cache.

Both orderings are correct. Choose whichever puts the more impressive element first.

## Bullet order within an entry

The bullets under one entry are read top to bottom by someone who does not yet know what
the work was. Order them so each bullet is comprehensible by the time it is reached.

**Lead with the bullet that establishes scope.** What was built, how large it was, what it
did. This is often the least impressive bullet in the group and it still goes first,
because it is the one that makes the others legible.

**End with the most specific and technical.** Diagnoses, optimizations, methodology
audits, anything that presupposes the reader already knows the system exists.

The failure mode is a strong diagnostic bullet placed first:

> Diagnosed a local-timestamp cursor silently dropping records and rebuilt it around an
> inclusive watermark, taking row loss from 1.8% to zero.

Every word is true and the reader has no idea what system this is, what it moves, or why
a cursor matters to it. The same sentence in second position, after the pipeline bullet
that names the sources and the nightly volume, lands completely.

This trades against the instinct to lead with the strongest claim. **Take the trade.** An
impressive bullet the reader cannot situate does not read as impressive, it reads as
jargon, and the seven-second scan does not include a second pass to reconstruct context.
Relevance between experiences is already expressed through bullet count and depth, per
`selection-rules.md` §4 — it does not also need to be expressed by bullet order inside an
entry.

Two consequences worth stating:

- **A build-then-refine pair goes build first**, even when the refinement carries the
  better metric.
- **Where one bullet supplies the dataset or system another one analyzes, it goes
  first.** The scraper before the finding, the pipeline before the tuning.

Single-bullet entries are exempt, and this says nothing about the order of entries
themselves, which stays reverse chronological.

## Recomposition

This is the point of the whole system. The records store X, Y, Z, scale, and tech as
separate fields precisely so you can choose what leads based on the job description.

Same record, two jobs:

```
STORED
  X: cut product catalog API latency
  Y: 800ms -> 95ms average, 14 queries
  Z: partial indexes + rewrote N+1 patterns, via pg_stat_statements
  scale: 2M-row table, 40k requests/day
  tech: PostgreSQL, Go, Datadog
```

> **JD emphasizes production debugging and performance:**
> Cut product catalog API latency from 800ms to 95ms by profiling 14 slow queries with
> pg_stat_statements and eliminating N+1 access patterns.

> **JD emphasizes large-scale data systems and SQL:**
> Tuned PostgreSQL access patterns on a 2M-row catalog serving 40k requests/day, adding
> partial indexes to cut average query latency 8x.

Same facts, different lead, different keywords surfaced. No fabrication — only
reselection and reordering of what the user supplied.

**Use `default_bullet` as-is when the job description already matches its natural
framing.** Recomposition is a tool, not an obligation.

## Mechanics

**No first person.** No "I", "me", "my", "we", "our". Start with a verb.

**Tense.** Past tense throughout, except the current role, which takes present tense.

**Articles.** Drop leading articles where it reads naturally — "Built pipeline
processing 2M records" is standard resume register. Do not strip so aggressively that it
reads as broken English.

**One line each.** Two is the maximum, and a two-line bullet must be genuinely worth the
extra line. A bullet wrapping to a third word on a second line wastes an entire line of
a scarce page — tighten it.

**Lead with a strong verb.** Built, designed, shipped, cut, migrated, automated,
diagnosed, scaled, refactored, instrumented, negotiated, led.

Avoid weak openers: *Responsible for, Helped with, Worked on, Assisted, Participated in,
Involved in, Tasked with, Contributed to.* Every one of these describes proximity to
work rather than performance of it.

**Ban empty intensifiers.** *Significantly, greatly, substantially, various, several,
numerous, cutting-edge, robust, seamless, leveraged, utilized, spearheaded,
synergized.* Readers discount adjectives and trust specifics. "Significantly improved
performance" is strictly weaker than "cut runtime 40%" and weaker even than "cut
runtime from 12 to 5 minutes" with no percentage at all.

Use "used", not "utilized".

**Numbers as numerals.** `14`, not `fourteen`. Numerals are higher contrast during a
scan.

**Format metrics for scanning.** Before-and-after beats a bare percentage: "800ms → 95ms"
carries more than "88% faster" because it reveals the scale of the system. Give both
when space allows.

**Weave keywords into bullets.** A technology named inside an accomplishment proves
application. The same technology in a skills list only asserts familiarity. When a job
description's key technology appears in a record, get it into a bullet.

## Truthfulness

**Never write a number that is not in a record.** Not an estimate, not a rounding, not a
plausible figure. If a bullet feels weak without a number, it stays weak.

**Never claim solo work that was collaborative.** Check the `role` field. "Contributed
to" is banned as a weak opener, but the underlying honesty is not optional — name what
the user personally did: "Built the retry and backoff layer for a team-owned payments
service" is both specific and honest.

**Never list a skill without backing.** Every technology in the skills section must
appear in `profile/skills.md` with a linked accomplishment.

**Do not upgrade titles.** If the record says "Software Engineer Intern", the resume
says that.

**Match the verb to the `origin` field.** Every accomplishment record carries `origin`,
recording who decided the approach. It constrains which verbs are honest:

| `origin` | Allowed | Not allowed |
| --- | --- | --- |
| `own` | designed, architected, devised, diagnosed, identified, built | — |
| `specified` | built, implemented, delivered, shipped, tested, extended | designed, architected, devised, pioneered |
| `assisted` | built, implemented, diagnosed, validated, directed | hand-rolled, wrote from scratch |

This is the difference between "I built X" and "I was told to build X and built it".
Both are real work; only the first supports a design verb. The failure mode is specific
and severe: a candidate who writes *designed* about a handed-down architecture gets asked
"why did you choose that approach?" and has no answer, which reads as either dishonesty
or shallowness.

Where `origin` is `specified` but the record's `context` names parts the user did decide,
build the bullet around those parts. That is the defensible ground, and it is usually
more interesting anyway — tuning something empirically and finding a non-obvious result
signals more than having drawn a box diagram.

## Summary section

Only for mid-level and above. New grads should not have one — it consumes four lines of
a scarce page to say what the education and experience sections already show.

When used: maximum four lines, no first person. State years of experience, domain
specialization, and one concrete distinguishing achievement.

> Backend engineer with 6 years building payment infrastructure at scale. Led the
> migration of a 40-service monolith to event-driven architecture, cutting p99 latency
> 60% while supporting 4x transaction growth.

## Skills section

Categorize. A comma-separated wall of 40 technologies is unreadable in seven seconds and
signals nothing about depth.

```
Languages: Python, Go, TypeScript, SQL
Frameworks: React, FastAPI, Node.js
Cloud & Infrastructure: AWS (EC2, S3, Lambda), Docker, Kubernetes, Terraform
Databases: PostgreSQL, Redis, MongoDB
```

Rules:

- Order categories by relevance to the job description, most relevant first
- Within a category, order by relevance, most relevant first
- Use the job description's exact strings where the user genuinely has the skill
- Give acronym-and-expansion once where both forms plausibly appear in a recruiter
  search: `Continuous Integration/Continuous Deployment (CI/CD)`
- Cap at roughly 4 categories and 6–8 items each
- Every item must be backed by evidence in `profile/skills.md`

Do not include skill levels ("Python — Expert"). Self-rated proficiency is noise and
invites the reader to disagree.

## Education

New grad: school, degree, major, graduation date, GPA if 3.5 or above. Relevant
coursework only if it evidences a job requirement the experience section misses.

Mid-level and above: school and degree only, at the bottom, and drop the graduation
year — a visible date invites age inference and adds nothing once experience carries the
document.

Honors, awards, and competitive results stay at any level. They are distinctive and
cheap in space.

## Projects

Each project entry's second line (the `entry()` `title` field) is the project's tech
stack, comma-separated — e.g. `Python, XGBoost, scikit-learn, pandas, NumPy` — never
`Personal` or the course/org affiliation. "Personal" wastes the line: it tells neither
reader anything, while the tech stack gets a second, denser pass of literal keyword
strings past both the ATS parser and the human scan. Pull the list from the record's
`tech` field; order it the way the job description would search for it when a job
requirement maps to this project.

If the course or organization context matters for a specific project (rare — usually
because the affiliation itself is a credential, like a recognizable lab or competition),
fold it into the project name or a bullet instead of spending the tech-stack line on it.
