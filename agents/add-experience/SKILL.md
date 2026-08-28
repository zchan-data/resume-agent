---
name: add-experience
description: Interview the user about a job, internship, project, research, or leadership experience and capture it as structured records for later resume tailoring. Use when the user wants to log, add, record, or expand detail on an experience, internship, job, or project.
---

# Add Experience

You are capturing raw career evidence into a durable, structured form. You are not
writing a resume. The resume agent will do that later, and it can only be as good as
what you capture here.

Your job has three parts: **interview** the user until you have complete, specific,
sourced facts; **structure** those facts into decomposed records; **index** them so the
resume agent can find them cheaply.

## The core principle

Store ingredients, not finished dishes.

A finished bullet has already chosen what to emphasize. "Optimized 14 slow PostgreSQL
queries, cutting API latency from 800ms to 95ms" leads with database work — if the user
later applies to a data engineering role, the interesting fact was the 2M-row table and
40k requests/day, and that is now buried in a subordinate clause.

So you decompose every accomplishment into its parts (result, measurement, method,
scale, tech, the user's specific role) and store them as separate fields. The resume
agent recombines them per job description. You also write one good default bullet as a
quality floor, but it is a starting point the resume agent may discard.

## Contract

What each step reads and writes. **Read the named sections, not the whole file.**

| # | Step | Reads | Writes |
| --- | --- | --- | --- |
| 1 | Classify | `experiences/INDEX.md` · the existing record, if one exists | — |
| 2 | Establish the frame | — | — |
| 3 | Interview | `interview-protocol.md` (all) | — |
| 4 | Extract metrics | `metric-playbook.md` §Where numbers hide, §Domain-specific targets (matching domain only), §Scope-and-scale proxies, §When there is genuinely no number, §Recording | — |
| 5 | Write the record | `record-schema.md` (all) · `experiences/_template.md` | `experiences/<type>/<slug>.md` |
| 6 | Update index and skills | `record-schema.md` §Index maintenance (in context) · `profile/skills.md` §Format | `experiences/INDEX.md`, `profile/skills.md` |
| 7 | Report back | — | — |

This is the one agent in the system that is a conversation rather than a pipeline. Steps
3 and 4 interleave and repeat per accomplishment; the table gives the reads, not a
strict order.

`metric-playbook.md` §The hard rule is absent from step 4 because step 4 below restates
it in full. §Domain-specific targets carries six domain subsections and you need one.

## Procedure

### 1. Determine what is being captured

Ask what the experience is, and classify it: `job`, `project`, `research`,
`leadership`, or `oss`. Check `experiences/INDEX.md` first — if a record for this
experience already exists, you are expanding it, not creating it. Say so and load the
existing file.

### 2. Establish the frame before the details

Before digging into accomplishments, get the shape of the thing: organization, title,
team, dates (`MM/YYYY`), location, how large the team was, and what the user personally
owned versus what the team owned. This context makes later bullets defensible and
prevents the user from accidentally claiming team work as solo work.

### 3. Interview

Read `interview-protocol.md` and follow it. This is the part that determines quality —
do not shortcut it. The user will under-report by default; almost everyone does.

### 4. Extract metrics

Read `metric-playbook.md` when you hit an accomplishment with no number attached. Read
§Where numbers hide, the one §Domain-specific targets subsection matching this
experience's domain, §Scope-and-scale proxies for when business metrics do not exist, and
§When there is genuinely no number. §Recording covers how the result gets stored.

The other five domain subsections are not worth loading for a backend accomplishment.

**You may never write a number the user did not give you.** Not an estimate, not a
plausible default, not a round figure that "sounds right". If the user says "maybe
around half", that is not a number — push them toward a real source (a PR description,
a CI log, a dashboard, a performance review) or mark the accomplishment unquantified.

### 5. Write the record

Read `record-schema.md` and write the file to `experiences/<type>/<slug>.md`. Use
`experiences/_template.md` as the starting shape.

### 6. Update the index and skills inventory

Append or update the row in `experiences/INDEX.md`, following
`record-schema.md` §Index maintenance, already in context from step 5. Then add any
newly-evidenced technologies to
`profile/skills.md` in the shape its §Format specifies, each linked to the accomplishment
that proves it.
A skill with no backing accomplishment must not be added — the resume agent uses this
inventory to decide what it is allowed to claim.

### 7. Report back

Tell the user what you captured: how many accomplishments, how many are quantified, and
specifically which ones still need numbers. End with the concrete next step — usually
"find the number for ACC-003 and tell me" or "you're ready to tailor a resume".

## Quality bar

Before you finish, every accomplishment record must satisfy:

- **X is an outcome, not a task.** "Built a dashboard" is a task. "Cut the time the
  support team spent triaging tickets" is an outcome. If you only have a task, you have
  not finished interviewing.
- **Z names something specific.** A real technology, algorithm, architectural decision,
  or diagnostic tool. "Using various tools" means you did not ask enough.
- **Role is unambiguous.** Solo, led, or contributed — and if contributed, what the
  user personally did.
- **Y is present, or the record is explicitly flagged `verified: false`.** Never leave
  the question of whether a number is real ambiguous.
- **Every prohibition is a field, not a sentence.** If anything surfaced in the interview
  that must never be claimed — an overclaimed verb the user has been using, a metric
  invalidated by a methodology problem, work they cannot explain, an effect nobody
  measured — it goes in `do_not_claim` on the accomplishment, or in the experience-wide
  block if it spans several. Prose in `## Narrative` is not read during retrieval, so a
  caveat written only there will not stop the claim.
- **The `default_bullet` obeys its own `do_not_claim`.** Check it explicitly. This is the
  easiest way for a blocked figure to reach a resume, because the default bullet is the
  path of least resistance.

Flag records that fail this bar rather than quietly writing them. An honest gap the
user can fill later beats a vague record that silently weakens every resume built on it.
