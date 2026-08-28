# Selection Rules

Deciding which experiences and which accomplishments earn space on one page.

## The scarcity

A one-page resume holds roughly 40–45 lines of content. After the header, skills,
and education, you have maybe 22–28 lines for experience and projects — call it 14 to 18
bullets total, across everything.

Selection is therefore the highest-leverage step in this whole system. A perfectly
written bullet about the wrong accomplishment is worth less than a plain bullet about
the right one.

## Procedure

### 1. Shortlist from the index

Read `experiences/INDEX.md`. Include an experience in the shortlist if any of:

- Its `domains` overlap the job's domain
- Its `tech` overlaps the job's keyword list
- It is recent and substantial regardless of domain (recency carries independent weight;
  an unexplained gap costs more than an off-domain entry)
- It is the user's most prestigious or recognizable organization

Read the `## Claims` section of the shortlisted records, not the whole files:
`python3 scripts/read-section.py -s Claims <files>`.

### 2. Score every accomplishment

Drop anything marked `claim: blocked` before scoring. It has no bullet, so its score is
irrelevant, and carrying it forward invites a late compromise when coverage looks thin.

For every remaining accomplishment, read its `do_not_claim` alongside its fields. A
prohibition changes what the accomplishment can evidence, which changes its Relevance
score. An accomplishment whose only tie to a Hard requirement runs through a prohibited
figure scores 0 on Relevance for that requirement, not 3.

Then score three axes 0–3.

**Relevance** — how directly does this evidence a stated requirement?
- 3: directly evidences a Hard requirement using the same technology
- 2: evidences a Hard requirement with transferable technology, or a Preferred one directly
- 1: evidences an Implied requirement, or demonstrates general engineering competence
- 0: unrelated

**Strength** — how convincing is it on its own?
- 3: verified metric, specific method, clear individual ownership
- 2: quantified but unverified, or verified but with diffuse ownership
- 1: unquantified, specific method, real outcome
- 0: unquantified and vague

Score Strength on the evidence that survives `do_not_claim`. An accomplishment with a
prohibited metric is a 1 at best, not a 3: for resume purposes it is unquantified.

**Distinctiveness** — how many other candidates can say this?
- 3: unusual scale, recognizable organization, real external adoption, competitive result
- 2: solid production work or a project with genuine users
- 1: coursework-grade or common tutorial territory
- 0: generic

Total = Relevance × 2 + Strength + Distinctiveness. Relevance is doubled deliberately:
a stunning accomplishment that does not speak to the job loses to a solid one that does.

### 3. Enforce coverage before maximizing score

Greedy selection by score alone produces a resume that hammers one requirement five
times and ignores three others. That fails, because a reader scanning for their
must-haves finds nothing on two of them.

So: **first**, for every Hard requirement, select the highest-scoring accomplishment that
evidences it. **Then** fill remaining space by score.

If a Hard requirement has no evidence at all, record it in the gap list. Do not stretch
an unrelated accomplishment to cover it.

### 4. Allocate space by experience

Bullets per experience, roughly:

| Experience | Bullets |
| --- | --- |
| Most relevant and recent role | 3–4 |
| Second role | 2–3 |
| Older or less relevant role | 1–2 |
| Lead project | 2–3 |
| Secondary project | 1–2 |

Reverse chronological order within each section. Never reorder by relevance — a reader
scanning the right margin for dates reads non-chronological order as concealment.

Relevance is expressed through *bullet count and depth*, not position.

### 5. Decide what to cut

Cut in this order when over budget:

1. Accomplishments scoring 0–1 on relevance
2. Second and third bullets on the least relevant experience
3. Older experiences entirely — but keep the line (org, title, dates) even with zero
   bullets rather than deleting it, if removing it would open a chronological gap
4. Coursework from Education
5. Projects, if professional experience already covers every Hard requirement

Never cut: contact information, the skills section, or anything that creates an
unexplained employment gap.

### 6. Record the gaps

Fill the `Evidence` and `Strength` columns in the requirements tables in
`match-analysis.md`, then append:

```markdown
## Selected

| ACC | Experience | Covers | Score | Bullets |
|---|---|---|---|---|

## Cut

| ACC | Reason |
|---|---|

## Gaps

| # | Requirement | Status |
|---|---|---|
```

Table cells only, one line each. `Status` is `unevidenced`, `thin`, or
`capture gap` — the last meaning the user may well have the experience and never logged
it, which is often the real fix.

**The strategy for each gap goes in `analysis-notes.md` → Gaps, and what to do about
them.** That is where you write whether to address it in the cover letter, build
something first, or run add-experience, and what it would take. It is the most useful
writing in the whole analysis and it is written for the user, so it must not sit in the
file the cover letter agent reloads in full. Same for any deliberate departure from the
scoring: the departure is a row in `## Selected`, the reasoning is a note.

`jd-analysis.md` §Output has the rule for deciding between the two files.

## Special cases

**No relevant experience at all.** Say so before writing. Offer to capture something
relevant, or to write the strongest honest resume while naming the gap. Do not proceed
silently.

**Too much relevant experience.** A good problem. Raise the relevance bar to 3 only,
and prefer verified metrics and recent work. Tell the user what strong material you cut
so they know it exists for other applications.

**One experience dominates.** If a single internship evidences everything, still include
a project or second experience — a resume drawing on one source reads as a narrow
candidate, and the reader has no way to judge whether the strength was the user or the
environment.

**Career-changer or off-domain.** Lead with transferable method and scale rather than
domain. A data pipeline is a data pipeline whether it moved genomics data or ad
impressions; name the shared structure explicitly rather than hoping the reader infers it.
