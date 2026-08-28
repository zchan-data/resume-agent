# Story Selection

Choosing the one or two things the letter magnifies.

## The scarcity

A cover letter holds 250 to 350 words. After the hook, the fit paragraph, and the close,
the evidence budget is roughly 150 to 200 words. That is one accomplishment told properly,
or one told properly plus one mentioned in a sentence.

The resume already lists everything. The letter exists to do the one thing a resume
cannot: take a single item and show the thinking behind it. Breadth here is pure waste,
because it duplicates a document the reader already has open.

## Selection procedure

### 1. Start from the existing analysis

If `match-analysis.md` is in the folder, the scoring is done. Look at the Hard
requirements and their evidence strengths, and at the "what this role actually optimizes
for" line. That line matters more than the requirement table for this decision: the letter
argues one thing, and it should argue the thing the team actually needs.

### 2. Pick the lead accomplishment

The lead should satisfy all four:

- **Covers a Hard requirement**, ideally the one the posting repeats most.
- **Has a verified or measured number.** A story without a number is a story about
  intentions.
- **Has depth behind it in the record.** Read `## Narrative` for the finalists:
  `python3 scripts/read-section.py -s Narrative <file>`. The `### ACC-NNN notes`
  subsection and the raw notes are where the texture is. If an accomplishment has no
  notes, there is nothing to magnify and the letter will just restate the resume in
  longer form.
- **Is defensible in an interview.** Check `origin` and `role`. The letter states this at
  more length than the resume does, so it invites more follow-up. Anything you write here,
  the user will be asked about.

When two candidates tie, prefer the one where something went wrong and got fixed.
Diagnosis stories are the most convincing narrative available, because they show the
process rather than the outcome, and process is what the reader is actually trying to
assess.

### 3. Pick the support, or decide not to

A second accomplishment earns its sentence only if it covers a different Hard requirement
than the lead. Two pieces of evidence for the same requirement is repetition.

Often the better use of that space is the fit paragraph. A letter with one deep story and
a genuine, specific reason for wanting this job beats a letter with two stories and a
generic closing.

### 4. Check against the resume

Open `resume.md` if it exists. Confirm:

- No sentence in the letter restates a bullet with the words rearranged.
- Every number, title, and date matches exactly.
- The letter's lead accomplishment is on the resume. The letter deepens the resume, it
  does not introduce parallel history the reader cannot cross-check.

## Turning a record into a paragraph

`## Claims` stores X, Y, Z, scale, role, and origin as separate fields. The resume agent
recomposes those into one line. The letter uses more of them, and adds what the resume
never touches: the accomplishment's `### ACC-NNN notes` in `## Narrative`.

Worked example, from `exp-acme-2026/ACC-001`:

```
X:        recovered order records a nightly warehouse sync was silently dropping
Y:        1.8% -> 0% row loss, measured across a 30-day replay
Z:        diagnosed a local-timestamp incremental cursor, rebuilt it around an inclusive
          watermark with a dedupe pass
scale:    ~40k orders/night, 3 upstream sources, 30-day replay
origin:   own (diagnosis and approach), assisted (script implementation)
notes:    the job reported success every night, so nothing surfaced the loss. Finding it
          required replaying a month of raw source files against the warehouse table by
          hand.
```

Resume bullet:

> Diagnosed silent row loss in a nightly order sync and rebuilt the incremental cursor
> around an inclusive watermark, eliminating 1.8% daily record loss across a 30-day replay
> of 40k-order batches.

Letter paragraph, same facts:

> The sync I built looked like it worked. It reported success every night, and it was
> quietly dropping about one order in fifty. There was no error and nothing to grep for,
> so I ended up replaying a month of raw source files against the warehouse table until I
> found the pattern: the incremental cursor was written against a local timestamp, and
> anything that landed in the hour the clocks moved never came back. I rebuilt the cursor
> around an inclusive watermark with a dedupe pass and replayed the same thirty days. Row
> loss went to zero.

What changed, and why:

- **The stakes come first.** "Looked like it worked" and "one order in fifty" set up why
  the diagnosis mattered. The resume has no room for stakes.
- **The narrative notes supply the texture.** Replaying a month of files by hand is the
  detail that makes it read as a memory rather than a claim, and it came from the record,
  not from imagination.
- **The number arrives last**, as the payoff, rather than leading as it does on a resume.
  The scan pattern that makes a leading metric correct on a resume does not apply to
  prose.
- **The verbs respect `origin`.** Diagnosed, added, ran. Not designed, not architected.
  See the origin table in `../tailor-resume/writing-rules.md`; it binds here too.
- **First person is fine.** This is the one place in the system where "I" is correct.

## When the record has no number

Say what happened concretely instead, and lean on scale and method:

> ...narrowed each nightly batch to the handful of records whose source rows had actually
> changed before anything reached the warehouse.

That is specific and true. What it must not become is "significantly reduced token usage"
or any other number-shaped phrase covering for a number you do not have. If the missing
number is worth having, tell the user in step 7 and point at
`experiences/INDEX.md`'s gap table. Several of the highest-value missing numbers in this
system are already listed there.

## What not to select

- **Anything carrying a `do_not_claim`, when the prohibition touches what you would
  magnify.** The `Claimable` column in the index and the `claim` field on each
  accomplishment flag these: metrics invalidated by train/test leakage, work that was
  AI-authored and is not the user's to claim. A letter states things at more length and
  with more confidence than a resume, which makes a blocked claim more dangerous here,
  not less. `claim: blocked` is never a candidate.
- **Anything the user cannot walk through for ten minutes.** The letter is an interview
  agenda. Whatever it magnifies is what they will be asked about first.
- **Anything requiring an explanation longer than the paragraph.** If the setup takes four
  sentences before the accomplishment lands, pick something else.
- **Team accomplishments where the user's own part is unclear.** Check `role`. In prose
  the ambiguity is more visible than on a resume, because prose has subjects.
