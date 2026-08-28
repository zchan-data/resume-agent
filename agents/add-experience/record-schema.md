# Record Schema

The on-disk format for an experience. Every field exists because the resume agent needs
it to make a decision.

## File location and naming

```
experiences/jobs/<year>-<org-slug>-<role-slug>.md        job, internship
experiences/projects/<year>-<project-slug>.md            personal or academic project
experiences/research/<year>-<lab-or-topic-slug>.md       research
experiences/leadership/<year>-<org-slug>.md              clubs, orgs, teaching
experiences/oss/<year>-<project-slug>.md                 open source contributions
```

One file per experience. Multiple accomplishments live inside one file.

## The two halves of a record

A record is split into `## Claims` and `## Narrative`, in that order.

**`## Claims` is read on every retrieval.** It holds the frontmatter-adjacent facts, the
one-line setting, the experience-wide prohibitions, and one structured block per
accomplishment. It must be self-sufficient: everything needed to shortlist, score, and
write a bullet lives here.

**`## Narrative` is read only for an accomplishment already selected**, or when writing
prose. It holds the full setting, per-accomplishment texture, raw notes, methodology
audits, and open metric opportunities.

The split exists because retrieval opens several records and uses a fraction of each.
`scripts/read-section.py -s Claims <files>` returns the head of many records at once.

**Prose is not a safe place for a prohibition.** If a claim must never be made, it goes
in a `do_not_claim` field in `## Claims`, not in a paragraph in `## Narrative`. A caveat
buried in prose is a caveat that gets skipped.

## Frontmatter

```yaml
---
id: exp-stripe-2025          # exp-<org-slug>-<year>, globally unique
type: job                    # job | project | research | leadership | oss
org: Stripe                  # organization, school, or "Personal" for solo projects
title: Software Engineer Intern
team: Payments Infrastructure  # omit if not applicable
location: San Francisco, CA    # or "Remote"
start: 06/2025               # MM/YYYY
end: 08/2025                 # MM/YYYY or "Present"
domains: [backend, distributed-systems]
tech: [Go, PostgreSQL, Kafka, AWS]
claimable: full              # full | partial | none
status: complete             # draft | complete
last_updated: 08/2026
---
```

`domains` drives retrieval — the resume agent filters on it before opening files. Use
values from the controlled list at the bottom of this document so filtering actually
works. `tech` should be the literal strings a job description would use.

`claimable` summarizes the record for the index:

- `full` — every accomplishment is usable as written
- `partial` — at least one accomplishment is `restricted` or `blocked`
- `none` — nothing here is the user's to claim

Mirror it into the `Claimable` column of `experiences/INDEX.md`, so shortlisting sees the
constraint before opening the file.

## The Claims section

### Setting and prohibitions

`## Claims` opens with two things:

```markdown
**Setting:** early-stage startup, 4-person engineering team. The user built the ingestion
service alone with one reviewer. Standalone deliverable, never merged to production.

**Do not claim (experience-wide):**

- **Architectural design of the pipeline.** The brief prescribed it; the user implemented
  it.
- **Deployment or user impact.** Not merged to production, not shipped to users.
```

The setting line is the compressed version of `## Narrative` → Setting, carrying only
what scoring needs: organization shape, team size, personal ownership, and whether the
work shipped. Distinctiveness cannot be judged without it.

The prohibition block is load-bearing. Write `- None.` when there are none, so its
absence is never ambiguous.

### Accomplishments

One block per accomplishment, numbered `ACC-001` upward, unique within the file.

```markdown
### ACC-001 — Query optimization on product catalog

- **claim:** ok
- **tags:** backend, performance, database
- **X (result):** cut product catalog API response latency
- **Y (measure):** 800ms -> 95ms average, across 14 queries
- **Z (method):** added partial indexes and rewrote N+1 query patterns, identified via pg_stat_statements
- **scale:** 2M-row table, ~40k requests/day
- **tech:** PostgreSQL, Go, Datadog
- **role:** solo
- **origin:** own
- **verified:** true
- **source:** PR #204
- **default_bullet:** Optimized 14 slow PostgreSQL queries identified via
  pg_stat_statements, adding partial indexes and rewriting N+1 patterns — cutting
  average API response time from 800ms to 95ms on the product catalog endpoint.
```

The per-accomplishment prose that used to live in a `context` field now goes to
`## Narrative` → `### ACC-001 notes`.

Field meanings:

- **claim** — whether this accomplishment can be used, and the first field for a reason.
  One of:
  - `ok` — usable as written, subject only to the verbs `origin` allows
  - `restricted` — usable, but something specific is off limits. `do_not_claim` says what
  - `blocked` — no honest bullet exists. `default_bullet` reads `BLOCKED — ...`

  A `restricted` accomplishment is still good material. The field is not a quality
  judgment; it separates what is true from what is defensible.
- **do_not_claim** — required whenever `claim` is `restricted` or `blocked`, omitted
  otherwise. Name the specific figure, verb, or assertion that is off limits and why in
  one clause. "R² and RMSE — leaked split" is enough; the reasoning goes in `## Narrative`.

  Write it as a prohibition, not a caution. "Be careful with the metrics" is not
  actionable at 2am on the fortieth application; "do not use R² 0.56" is.
- **tags** — retrieval keywords. Lowercase, kebab-case. Overlap with `domains` is fine.
- **X** — the outcome, stated as a result rather than a task. What became true.
- **Y** — the measurement, with units and direction. Before-and-after beats a bare
  percentage. Omit the field entirely if unquantified; do not write "N/A".
- **Z** — the method: the specific technology, algorithm, pattern, or diagnostic tool.
  This is what makes a bullet credible. Vague Z means an incomplete interview.
- **scale** — size of the system or problem, independent of the improvement. Often the
  most impressive fact and the one users most reliably forget to mention.
- **tech** — technologies used in *this specific accomplishment*, not the whole job.
- **role** — `solo`, `led (N-person team)`, or `contributed` plus what the user
  personally did. Protects the user from over-claiming in an interview.
- **origin** — who decided the approach. One of:
  - `own` — the user identified the problem and chose the solution
  - `specified` — the approach was handed to the user in a spec, ticket, or brief
  - `assisted` — implementation was AI-assisted or heavily reference-driven, with the
    user directing and validating

  This field exists because "I built X" and "I was told to build X and built it" are
  different claims, and only the first supports a bullet verb like *designed* or
  *architected*. Both are legitimate work. Conflating them is how a candidate ends up
  unable to answer "why did you choose that approach?" in an interview. When `origin` is
  `specified`, note in the accomplishment's `## Narrative` notes exactly which parts the
  user did decide — that is where the defensible bullet lives.

  `assisted` is not a demerit. Directing an AI to implement a fix you diagnosed and
  validated is ordinary engineering practice; the field just keeps the record accurate
  about what the user personally typed.

  `agent-generated` is different in kind and always pairs with `claim: blocked`. The
  user did not author the work and cannot explain it, so no verb is available. Set
  `role` to `directed only`.
- **verified** — the status of `Y`. One of:
  - `true` — the number traces to a system of record (dashboard, CI log, PR, stored test)
  - `measured` — the user measured it themselves but it is not stored anywhere reusable
  - `false` — recollection only, or no number exists

  `measured` is common and honest: a one-off manual comparison producing a real number.
  It is resume-usable. It matters because if an interviewer asks to see the evaluation,
  `true` can be shown and `measured` has to be re-run.
- **source** — where the metric came from. Required whenever `Y` is present.
- **default_bullet** — one ready-to-use XYZ bullet, written at capture time. A quality
  floor, not a constraint. Follow `tailor-resume/writing-rules.md` when writing it.

  **It must satisfy this accomplishment's own `do_not_claim`.** A default bullet is the
  path of least resistance onto a resume, so a prohibited figure sitting inside one is
  the most likely way a blocked claim ships. Write the bullet, then read the
  prohibition, then check the bullet against it.

## The Narrative section

Everything below is prose the resume agent does not read during retrieval.

### Setting

Two to four sentences. What the organization does, what the team owned, what the user
was hired to do, team size, and who they reported to. This never appears on a resume
directly — it exists so the resume agent can judge whether an accomplishment is
impressive for the setting, and so the user can rebuild the story for an interview.

The compressed one-line version goes in `## Claims`.

### ACC-NNN notes

One subsection per accomplishment that has anything worth saying: why it mattered, what
was hard, what the user learned, who noticed. Free prose.

This is what the cover letter agent mines. A record whose accomplishment has no notes
has nothing to magnify into a paragraph, and the letter will just restate the resume.

Reasoning behind a `do_not_claim` belongs here too. The field states the prohibition; the
notes explain it.

### Raw notes

Anything the user said that did not fit a field. Do not discard it — future agents
(cover letter, outreach) will want the texture, and re-composition sometimes needs a
detail the schema did not anticipate.

### Open metric opportunities

Numbers that do not exist yet but are recoverable, ranked by how much they would
strengthen the record. Each entry names the number and how to get it.

This section is what turns an unquantified record into a quantified one over time.
Without it, a gap identified during the interview is forgotten the moment the
conversation ends. Mirror each entry into the gap table at the bottom of
`experiences/INDEX.md` so it is visible without opening the file.

## Index maintenance

After writing or editing a record, update `experiences/INDEX.md`. The resume agent reads
only the index first, so a missing row means the experience is invisible to tailoring.

Carry the frontmatter `claimable` value into the `Claimable` column, and keep the
`Headline` column to the single most impressive fact. Prohibitions belong in the column
built for them and in the record's `do_not_claim` fields, not smuggled into the headline
prose where a scanning agent may read past them.

## Controlled vocabulary: domains

Use these values so filtering is reliable. Add new ones only when nothing fits, and add
them to this list at the same time.

`backend`, `frontend`, `fullstack`, `mobile`, `distributed-systems`, `infrastructure`,
`devops`, `sre`, `data-engineering`, `machine-learning`, `data-science`, `security`,
`embedded`, `graphics`, `compilers`, `product`, `design`, `research`, `teaching`,
`leadership`
