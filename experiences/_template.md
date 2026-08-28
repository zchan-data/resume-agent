---
id: exp-<org-slug>-<year>
type: <job | project | research | leadership | oss>
org:
title:
team:
location:
start: MM/YYYY
end: MM/YYYY
domains: []
tech: []
claimable: <full | partial | none>
status: draft
last_updated: MM/YYYY
---

<!--
The record is split in two. `## Claims` is everything retrieval needs and is what the
resume agent reads. `## Narrative` is prose it reads only for an accomplishment already
selected. Keeping them apart is what makes retrieval cheap; do not move prose up.
-->

## Claims

**Setting:** one or two lines. Organization shape, team size, what the user personally
owned, and whether the work shipped. This is the minimum needed to judge whether an
accomplishment is impressive for its setting. The full version goes in `## Narrative`.

**Do not claim (experience-wide):**

<!--
Every prohibition that applies across the whole experience: overclaimed verbs, metrics
invalidated by a methodology defect, work the user did not author, effects never
measured. If there are none, write `- None.`

This block is load-bearing. It is read on every retrieval, and it is the only thing
standing between a buried caveat and a fabricated claim. A prohibition that lives only
in prose will be missed.
-->

- 

### ACC-001 — <short handle>

- **claim:** <ok | restricted | blocked>
- **do_not_claim:** <omit entirely when claim is ok>
- **tags:**
- **X (result):**
- **Y (measure):**
- **Z (method):**
- **scale:**
- **tech:**
- **role:**
- **origin:**
- **verified:**
- **source:**
- **default_bullet:**

<!--
Omit the Y and source fields entirely if unquantified — do not write "N/A" — and set
verified: false.

X is an outcome, not a task. Z names something specific. Role is unambiguous.
origin is own | specified | assisted | agent-generated. verified is true | measured | false.
See agents/add-experience/record-schema.md for full field definitions.
-->

## Narrative

Read this section only for an accomplishment already selected, or when writing prose.

### Setting

<!--
Two to four sentences. What the organization does, what the team owned, what the user
was hired to do, team size, reporting line. Never appears on a resume directly — it
exists so the resume agent can judge whether an accomplishment is impressive for its
setting, and so the user can rebuild the story for an interview.
-->

### ACC-001 notes

<!--
Anything that did not fit the structured fields: why it mattered, what was hard, what
the user learned, who noticed. This is the field the cover letter agent mines for
texture. One subsection per accomplishment that has any.
-->

### Raw notes

<!--
Anything the user said that did not fit a field. Do not discard it — recomposition
sometimes needs a detail the schema did not anticipate, and future agents will want
the texture.
-->

### Open metric opportunities

<!--
Recoverable numbers, ranked by value. Name the number and how to get it.
Mirror each into the gap table at the bottom of experiences/INDEX.md.
-->
