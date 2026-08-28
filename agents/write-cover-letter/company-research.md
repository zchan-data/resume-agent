# Company Research

Gathering the specific, sourced facts that make a letter unmistakably written for one
company.

## Why this step exists

Anyone can generate a fluent letter in four seconds. What nobody can generate is proof
that a human spent twenty minutes reading about the company. That proof is the only thing
in the letter a competing applicant cannot mass-produce, and recruiters have learned to
look for it first because it is the cheapest way to sort effort from volume.

One concrete, correct, non-obvious detail about the company outperforms three paragraphs
of enthusiasm. It also does something enthusiasm cannot: it demonstrates the candidate
can find and absorb unfamiliar technical context, which is most of the job.

## The fabrication rule

Every claim about the company in the letter must trace to a line in this file with a
source. No exceptions, and this is stricter than it sounds:

- Not "they recently raised a Series B" unless you have the announcement.
- Not "your engineering blog post about the migration" unless you have the post.
- Not the hiring manager's name unless you found it. A wrong name is worse than no name.
- Not a product feature you inferred from the job description. Inference is not research,
  and the reader knows their own product.

The asymmetry is brutal. A correct specific detail buys a few seconds of goodwill. An
incorrect one ends the application, because the reader concludes either that the
candidate is careless or that a model wrote it unsupervised. Both are disqualifying.

**When in doubt, cut the claim.** A letter with two verified details and no third is
strictly better than one with three details and a guess.

## What to look for

Ranked by how much signal each carries. Two or three good items are enough. Stop when
you have them.

| Rank | What | Why it lands |
| --- | --- | --- |
| 1 | Engineering blog post, tech talk, public postmortem, or open-source repo | Proves the candidate read something technical and voluntary. Highest signal available, and vanishingly rare in an applicant pool. |
| 2 | A specific product surface or recent shipped feature the role touches | Shows the candidate knows what the team actually builds, not what the marketing page says. |
| 3 | The company's stated technical approach or constraint | Lets the letter connect the candidate's method to their problem rather than to their industry. |
| 4 | Funding round, expansion, new market, scale milestone | Dates the letter and grounds a pain hypothesis. Weaker alone: it is the first thing every applicant finds. |
| 5 | Hiring manager or team lead name and background | Fixes the salutation and can open a hook. Only if verifiable. |

Skip the mission statement. Every applicant quotes it, so it carries no information, and
quoting it reads as having found nothing else.

## Where to look

Use web search and fetch if the tools are available in the session:

- The company's engineering blog and their GitHub organization
- The job description itself, read a second time for technical specifics rather than
  requirements: named systems, scale figures, stated constraints
- Recent press or funding announcements
- Conference talks or podcast appearances by their engineers
- The careers page for how the team describes itself

If web tools are not available, or turn up nothing usable, **ask the user.** They chose
this company for a reason, and that reason is usually a better hook than anything a
search returns. Good questions:

- What made you apply here rather than somewhere else? Be specific.
- Do you use the product, or have you read anything they published?
- Do you know anyone there, or has anyone described the team to you?
- Is there something about the problem they work on that you actually find interesting?

The user's genuine, idiosyncratic reason is the most valuable input this step can
produce. It is also the one thing in the letter that is guaranteed to be true and
guaranteed to be theirs. Ask for it even when the search went well.

## Finding the addressee

Try, in order: the job description, the careers page, LinkedIn for the team's engineering
manager, the company blog's author bylines, a recruiter named in the posting.

If you find a name you are confident in, use it. If you do not, use the team
(`Dear Northwind Robotics Operations Team`) or the plain fallback (`Dear Hiring Manager`).

Never `To Whom It May Concern`. It reads as a form letter because it is the salutation of
a form letter.

Never guess a name from a pattern or a plausible-sounding title. Getting a person's name
wrong in the first line is the most expensive possible error in the document.

## Handling redaction

Some ATS platforms anonymize applications before a human sees them, stripping names,
demographics, and sometimes the school. Assume it may happen.

The practical consequence: the letter cannot lean on the university, the recognizable
employer name, or any personal narrative as its load-bearing argument. Those may be
removed. What survives redaction is the technical substance, the specific problem solved,
the number attached to it, and the reasoning. Build the argument out of those, and let
the recognizable names be a bonus when they do come through.

## Output

Write `company-research.md` into the application folder.

```markdown
# Company Research: <Company>

## Sourced facts

| # | Fact | Source | Usable how |
|---|---|---|---|
| C1 | | | hook / pain hypothesis / fit paragraph |

## Addressee

- Name:
- Title:
- Source:
- Confidence: high / medium / none. If not high, fall back to <team name>.

## The user's own reason for applying

<Verbatim, or close to it. This is raw material for the fit paragraph and it must stay
in the user's words as far as possible.>

## Considered and rejected

<Anything you found but chose not to use, and why. Usually: too generic, everyone will
cite it, or could not verify.>

## Could not verify

<Things worth including if the user can confirm them.>
```

Keep the "considered and rejected" section. On a re-run it stops you rediscovering the
same weak detail, and it shows the user what the search actually surfaced.
