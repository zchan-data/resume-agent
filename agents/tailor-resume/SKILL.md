---
name: tailor-resume
description: Turn a job description into a tailored, ATS-safe one-page resume drawn from captured experience records, rendered to PDF via Typst. Use when the user pastes a job description or asks to tailor, generate, edit, or re-render a resume for a specific role.
---

# Tailor Resume

You are engineering a document that must survive two very different readers: a parser
that strips formatting and matches literal strings, and a human who will spend roughly
seven seconds deciding whether to keep reading.

Everything in this skill exists to serve those two readers at once.

## Hard constraints

- **Read only from `experiences/` and `profile/`. Write only into `resumes/`.** If a
  job description demands evidence that does not exist in the records, that is a gap to
  report — never a gap to fill with invention.
- **Every claim traces to a record.** Each bullet must map to a specific `ACC-NNN`. Each
  skill listed must appear in `profile/skills.md` with backing evidence.
- **`do_not_claim` overrides everything, including `default_bullet`.** A record's
  prohibitions bind even when the job description asks for exactly the thing they block.
  A `blocked` accomplishment produces no bullet at all. See system invariant 8.
- **Stop at the draft.** `resume.md` is an approval gate. Never render a PDF until the
  user has seen the markdown and approved it.
- **Never invent.** No metric, title, date, or technology the user did not supply.

## Contract

What each step reads and writes. **Read the named sections, not the whole file.** These
rule files are long and most of each one does not apply to the step that cites it.

| # | Step | Reads | Writes |
| --- | --- | --- | --- |
| 1 | Set up folder | — | `job-description.md` |
| 2 | Analyze the JD | `jd-analysis.md` (all) | `match-analysis.md`, `analysis-notes.md` |
| 3 | Retrieve evidence | `experiences/INDEX.md`, then `## Claims` of matching records only · `profile/identity.md` §Career stage | — |
| 4 | Select and map | `selection-rules.md` (all) | `match-analysis.md` (append), `analysis-notes.md` (append) |
| 5 | Write the draft | `format-rules.md` §Non-negotiable ATS rules, §Page budget, §Section order (one variant), §Contact header, §Never do · `writing-rules.md` §The bullet formula, §Bullet order within an entry, §Recomposition, §Mechanics, §Truthfulness, plus one section rule per resume section present · `profile/identity.md` §Contact, §Logistics · `profile/skills.md` §Inventory, §Claimed but unevidenced · `profile/education.md` | `resume.md` |
| 6 | Stop and present | — | — |
| 7 | Render | `render.md` (all) · `format-rules.md` §Whitespace and typography | `resume.typ`, `resume.pdf` |
| 8 | Verify | already in context from step 7 | — |

Two absences from step 5 are deliberate. `format-rules.md` §The two readers is restated in
this file's opening, and §Whitespace and typography governs the Typst template, so it is
only actionable at render time.

## Procedure

### 1. Set up the application folder

Create `resumes/<YYYY-MM-DD>-<company-slug>-<role-slug>/` and save the job description
verbatim as `job-description.md`. Verbatim matters — you will return to it for literal
keyword strings, and a paraphrase loses exactly the strings the ATS matches on.

If the user pasted an application URL, save it in the frontmatter of that file.

### 2. Analyze the job description

Read `jd-analysis.md` and follow it. Its §Templates give the exact shape of the two
output files.

The analysis is split by reader, and `jd-analysis.md` §Output has the rule for deciding
which file a sentence belongs in. `match-analysis.md` holds tables and short lists and is
reloaded by the cover letter agent, so it stays at roughly 90 lines. `analysis-notes.md`
holds the reasoning, is written for the user, and is never loaded by an agent.

This step produces a requirements table and a keyword list. Do not skip ahead to writing
— tailoring that is not grounded in an explicit requirements extraction degenerates into
lightly reworded boilerplate.

### 3. Retrieve candidate evidence

Read `experiences/INDEX.md` first. Filter to plausible experiences by domain and tech
overlap, then read the `## Claims` section of those records and nothing else:

```bash
python3 scripts/read-section.py -s Claims experiences/projects/foo.md experiences/jobs/bar.md
```

`## Claims` carries every field selection needs plus the prohibitions. `## Narrative` is
prose for the cover letter agent and for interview prep; it does not inform a resume
bullet. Do not read every experience file, and do not read whole files — the index and
the split both exist to keep this cheap.

Note the `Claimable` column as you shortlist. A `partial` record is usually still worth
opening; it means the constraints are in the `do_not_claim` fields, which you will have
in front of you.

Also read `profile/identity.md` §Career stage here. It decides which section-order
variant step 5 uses, and knowing it now means step 5 loads one variant instead of three.

### 4. Select and map

Read `selection-rules.md`. Build the coverage matrix mapping each job requirement to
the accomplishment that evidences it, select what makes the page, and identify gaps.

The tables append to `match-analysis.md`. The reasoning behind them, and what the user
should do about each gap, appends to `analysis-notes.md`.

### 5. Write the draft

Write `resume.md`.

`format-rules.md` governs section order, page budget, and everything ATS-related. Read
§Non-negotiable ATS rules, §Page budget, §Contact header, §Never do, and the one
§Section order variant that matches the career stage you read in step 3.

`writing-rules.md` governs how individual bullets are constructed. Read
§The bullet formula, §Bullet order within an entry, §Recomposition, §Mechanics, and
§Truthfulness. Those five apply to every bullet. Then read one further section per resume
section you are actually writing:
§Summary section, §Skills section, §Education, §Projects. A new-grad resume has no
summary, so §Summary section is not read.

Pull contact details from `profile/identity.md` §Contact, relocation intent from
§Logistics, the skills list from `profile/skills.md` §Inventory, and the education entry
from `profile/education.md`. Check `profile/skills.md` §Claimed but unevidenced before
listing anything — that section is what you are forbidden to claim.

### 6. Stop and present

Show the user the draft. Report, concisely:

- Which experiences made the cut and which were left out, with the reason
- Which job requirements you could not evidence
- Any place you wanted a metric and did not have one
- Anything you deliberately cut for space that they might want back

Then wait. Do not render.

### 7. Render on approval

Once approved, read `render.md` and produce `resume.typ` and `resume.pdf`. Read
`format-rules.md` §Whitespace and typography now if you did not at step 5 — it holds the
vertical-rhythm ordering the template's spacing constants must preserve, and it is the
only part of that file that matters at render time.

If the user hand-edited `resume.md`, render from their edited version. Never regenerate
the draft from scratch after they have touched it without asking first.

### 8. Verify the output

After compiling, extract the PDF's text layer and confirm it reads in linear order with
contact details intact. `render.md` §Verification covers how, and is already in context
from step 7. A PDF that looks right but extracts wrong is the specific failure mode this
whole system is built to avoid.

## Re-running

If the user returns to an existing application folder wanting changes, do not rebuild
from zero. Read the existing `match-analysis.md` and `resume.md`, make the targeted
change, and re-render. The analysis is expensive and still valid.

## When the evidence is thin

If the records genuinely cannot support the role — a backend job description against a
candidate with only frontend evidence — say so directly before writing. Offer to run
the add-experience agent to capture something relevant, or to write the strongest honest
resume available while naming the gap.

Do not quietly stretch existing evidence to cover requirements it does not meet. A
resume that wins an interview it cannot survive is worse than no interview.

## Deferred: ATS-specific handling

The research supports per-platform tuning (Workday and Taleo parse strictly and prefer
DOCX; Greenhouse, Lever, and Ashby handle single-column PDFs well). It is not
implemented, because the universal format in `format-rules.md` parses at 95–99% across
all of them and the only decision detection would drive is PDF versus DOCX.

**Turn this on when a DOCX renderer exists.** At that point, detect from the application
URL: `myworkdayjobs.com` and Taleo instances get DOCX; `greenhouse.io`, `lever.co`, and
`ashbyhq.com` get PDF.
